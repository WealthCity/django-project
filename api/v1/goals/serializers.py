import copy
import logging

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_framework.fields import FloatField, IntegerField

from main.models import (
    ClientAccount,
    Goal, GoalSetting, GoalMetric, GoalTypes,
    Position, Portfolio, PortfolioItem,
    RecurringTransaction,
    StandardAssetFeatureValues,
    Transaction, TRANSACTION_REASON_DEPOSIT)
from portfolios.management.commands.portfolio_calculation import (
    get_instruments, calculate_portfolio, Unsatisfiable,
    current_stats_from_weights)
from portfolios.management.commands.risk_profiler import recommend_risk


__all__ = (
    'GoalSerializer',
    'GoalListSerializer',
    'GoalUpdateSerializer',
    'GoalTypeListSerializer',
)


logger = logging.getLogger('goal_serializer')


# TODO: too messy module. deeply refactor later.


class PortfolioItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioItem
        fields = (
            'asset',
            'weight',
        )


class PortfolioSerializer(serializers.ModelSerializer):
    items = PortfolioItemSerializer(many=True)

    class Meta:
        model = Portfolio
        fields = (
            'stdev',
            'er',
            'items',
        )
        # Variance and er are read only because they are ALWAYS calculated from backend using our data.
        read_only_fields = (
            'stdev',
            'er'
        )


class StatelessPortfolioItemSerializer(serializers.Serializer):
    asset = IntegerField()
    weight = FloatField()
    volatility = FloatField()


class PortfolioStatelessSerializer(serializers.Serializer):
    stdev = FloatField()
    er = FloatField()
    items = StatelessPortfolioItemSerializer(many=True)


class RecurringTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringTransaction
        fields = (
            'recurrence',
            'enabled',
            'amount',
        )


class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'amount',
            'from_goal',
            'to_goal',
        )
        required_fields = (
            'amount'
        )

    #def create(self, validated_data):
    #    return Transaction.objects.create(**validated_data)

    def update(self, validated_data):
        raise NotImplementedError('update is not a valid operation for a Transaction')


class GoalMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalMetric
        exclude = (
            'id',
            'setting',
        )


class GoalMetricCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalMetric


class GoalSettingSerializer(serializers.ModelSerializer):
    metrics = GoalMetricSerializer(many=True)
    recurring_transactions = RecurringTransactionSerializer(many=True)
    portfolio = PortfolioSerializer()

    class Meta:
        model = GoalSetting
        fields = (
            'target',
            'completion',
            'hedge_fx',
            'metrics',
            'recurring_transactions',
            'portfolio',
        )

    def update(self, setting, validated_data):
        """
        Overwrite update to deal with nested writes.
        :param instance:
        :param validated_data:
        :return:
        """
        goal = validated_data.pop('goal')
        metrics_data = validated_data.pop('metrics', None)
        tx_data = validated_data.pop('recurring_transactions', None)
        port_data = validated_data.pop('portfolio', None)

        with transaction.atomic():
            if port_data is None:
                # We have to do it this way so the portfolio_id field on the setting is updated.
                new_port = setting.portfolio
                pxs = setting.portfolio.items.all()
                # Get the current portfolio statistics of the current weights,, as new weights were not passed in.
                er, stdev, idatas = current_stats_from_weights([(item.asset.id, item.weight) for item in pxs])
                new_port.id = None
                new_port.er = er
                new_port.stdev = stdev
                new_port.save()
                setting.portfolio = new_port
                for item in pxs:
                    item.portfolio = setting.portfolio
                    item.volatility = idatas[item.id]
                    item.save()
            else:
                old_port = setting.portfolio
                port_items_data = port_data.pop('items', None)
                # Get the current portfolio statistics of the given weights.
                er, stdev, idatas = current_stats_from_weights([(item['asset'],
                                                                 item['weight']) for item in port_items_data])
                setting.portfolio = Portfolio.objects.create(er=er, stdev=stdev)
                PortfolioItem.objects.bulk_create([PortfolioItem(portfolio=setting.portfolio,
                                                                 **i_data,
                                                                 volatility=idatas[i_data['asset']]) for i_data in port_items_data])
                old_port.delete()

            for attr, value in validated_data.items():
                setattr(setting, attr, value)

            # We need to save these before we change the id.
            txs = setting.recurring_transactions.all()
            mxs = setting.metrics.all()

            # Change the id so we create a new item on save.
            setting = copy.copy(setting)
            setting.pk = None
            setting.save()

            if tx_data is None:
                for item in txs:
                    item.setting = setting
                    item.save()
            else:
                RecurringTransaction.objects.bulk_create([RecurringTransaction(setting=setting, **i_data) for i_data in tx_data])

            if metrics_data is None:
                for item in mxs:
                    item.setting = setting
                    item.save()
            else:
                GoalMetric.objects.bulk_create([GoalMetric(setting=setting, **i_data) for i_data in metrics_data])

            goal.set_selected(setting)

        return setting

    def create(self, validated_data):
        # TODO: Remove this method once all goals have selected-settings
        """
        Puts the passed settings into the 'selected_settings' field on the passed goal.
        """
        goal = validated_data.pop('goal')
        metrics_data = validated_data.pop('metrics')
        tx_data = validated_data.pop('recurring_transactions')
        port_data = validated_data.pop('portfolio')
        port_items_data = port_data.pop('items')
        with transaction.atomic():
            # Get the current portfolio statistics of the given weights.
            er, stdev, idatas = current_stats_from_weights([(item['asset'],
                                                             item['weight']) for item in port_items_data])
            port = Portfolio.objects.create(er=er, stdev=stdev)
            PortfolioItem.objects.bulk_create([PortfolioItem(portfolio=port,
                                                             **i_data,
                                                             volatility=idatas[i_data['asset']]) for i_data in port_items_data])
            setting = GoalSetting.objects.create(portfolio=port, **validated_data)
            RecurringTransaction.objects.bulk_create([RecurringTransaction(setting=setting, **i_data) for i_data in tx_data])
            GoalMetric.objects.bulk_create([GoalMetric(setting=setting, **i_data) for i_data in metrics_data])
            goal.set_selected(setting)

        return setting

    # TODO: REactivate after all goals have selected_settings
    #def create(self, validated_data):
    #    raise NotImplementedError('create is not a valid operation for a GoalSetting')


class GoalSettingStatelessSerializer(serializers.ModelSerializer):
    """
    Creates a goal setting that has no database representation, but is linked to the real goal.
    We use the ModelSerializer to do all our field representation for us.
    """
    metrics = GoalMetricSerializer(many=True)
    recurring_transactions = RecurringTransactionSerializer(many=True)

    class Meta:
        model = GoalSetting
        fields = (
            'target',
            'completion',
            'hedge_fx',
            'metrics',
            'recurring_transactions',
        )

    def save(self):
        raise NotImplementedError('Save is not a valid operation for a stateless serializer')

    def update(self):
        raise NotImplementedError('update is not a valid operation for a stateless serializer')

    def create(self):
        raise NotImplementedError('create is not a valid operation for a stateless serializer')

    @staticmethod
    def create_stateless(validated_data, goal):
        metrics_data = validated_data.pop('metrics')
        tx_data = validated_data.pop('recurring_transactions')
        port = Portfolio(stdev=0, er=0)
        setting = GoalSetting(portfolio=port, **validated_data)
        metrics = [GoalMetric(setting=setting, **i_data) for i_data in metrics_data]
        goalt = goal

        # Currently unused
        #RecurringTransaction.objects.bulk_create([RecurringTransaction(setting=setting, **i_data) for i_data in tx_data])

        class DummySettings(object):
            class PseudoManager:
                @staticmethod
                def all(): return metrics
            id = None
            goal = goalt
            metrics = PseudoManager
            target = setting.target
            completion = setting.completion
            hedge_fx = setting.hedge_fx

        return DummySettings()


class GoalSerializer(serializers.ModelSerializer):
    """
    For read (GET) requests only
    """
    class InvestedSerializer(serializers.Serializer):
        deposits = serializers.FloatField()
        withdrawals = serializers.FloatField()
        other = serializers.FloatField()

    class EarnedSerializer(serializers.Serializer):
        market_moves = serializers.FloatField()
        dividends = serializers.FloatField()
        fees = serializers.FloatField()

    # property fields
    on_track = serializers.BooleanField()
    balance = serializers.FloatField(source='current_balance')
    earnings = serializers.FloatField(source='total_earnings')
    stock_balance = serializers.FloatField()
    bond_balance = serializers.FloatField()
    total_return = serializers.FloatField()
    invested = InvestedSerializer(source='investments')
    earned = EarnedSerializer(source='earnings')
    selected_settings = GoalSettingSerializer()

    class Meta:
        model = Goal


class GoalListSerializer(serializers.ModelSerializer):
    """
    For read (GET) requests only
    Light version of GoalSerializer
    """
    on_track = serializers.BooleanField()
    balance = serializers.FloatField(source='current_balance')
    earnings = serializers.FloatField(source='total_earnings')
    selected_settings = GoalSettingSerializer()

    class Meta:
        model = Goal


class GoalCreateSerializer(serializers.ModelSerializer):
    """
    For write (POST/...) requests only
    """
    target = serializers.IntegerField()
    completion = serializers.DateField()
    initial_deposit = serializers.IntegerField(required=False)
    ethical = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = Goal
        fields = (
            'account',
            'name',
            'type',
            'target',
            'completion',
            'initial_deposit',
            'ethical',
        )  # list fields explicitly

    def __init__(self, *args, **kwargs):
        super(GoalCreateSerializer, self).__init__(*args, **kwargs)

        # request-based validation
        request = self.context.get('request')
        if not request:
            return # for swagger's dummy calls only

        user = request.user

        # experimental / for advisors
        if user.is_advisor:
            self.fields['account'].queryset = \
                self.fields['account'].queryset.filter_by_advisor(user.advisor)

        # experimental / for clients
        # TEMP set default account
        if user.is_client:
            self.fields['account'].required = False
            self.fields['account'].default = user.client.accounts.all().first()
            self.fields['account'].queryset = \
                self.fields['account'].queryset.filter_by_client(user.client)

    def create(self, validated_data):
        """
        Override the default create because we need to generate a portfolio.
        :param validated_data:
        :return: The created Goal
        """
        account = validated_data['account']

        idata = get_instruments()

        with transaction.atomic():
            portfolio = Portfolio.objects.create(
                stdev=0,
                er=0,
            )
            settings = GoalSetting.objects.create(
                target=validated_data['target'],
                completion=validated_data['completion'],
                hedge_fx=False,
                portfolio=portfolio,
            )
            goal = Goal.objects.create(
                account=account,
                name=validated_data['name'],
                type=validated_data['type'],
                portfolio_set=account.default_portfolio_set,
                selected_settings=settings,
            )

            # Based on the risk profile, and whether an ethical profile was specified on creation, set up Metrics.
            recommended_risk = recommend_risk(settings)
            GoalMetric.objects.create(setting=settings,
                                      type=GoalMetric.METRIC_TYPE_RISK_SCORE,
                                      comparison=GoalMetric.METRIC_COMPARISON_EXACTLY,
                                      rebalance_type=GoalMetric.REBALANCE_TYPE_ABSOLUTE,
                                      rebalance_thr=0.05,
                                      configured_val=recommended_risk)
            if validated_data['ethical']:
                GoalMetric.objects.create(
                    setting=settings,
                    type=GoalMetric.METRIC_TYPE_PORTFOLIO_MIX,
                    feature=StandardAssetFeatureValues.SRI_OTHER.get_object(),
                    comparison=GoalMetric.METRIC_COMPARISON_EXACTLY,
                    rebalance_type=GoalMetric.REBALANCE_TYPE_ABSOLUTE,
                    rebalance_thr=0.05,
                    configured_val=1  # Start with 100% ethical.
                )

            # Add the initial deposit if specified.
            initial_dep = validated_data.pop('initial_deposit', None)
            if initial_dep is not None:
                Transaction.objects.create(reason=TRANSACTION_REASON_DEPOSIT,
                                           to_goal=goal,
                                           amount=initial_dep)

            # Calculate the optimised portfolio
            try:
                weights, er, stdev = calculate_portfolio(settings, idata)
                items = [PortfolioItem(portfolio=portfolio,
                                       asset=idata[2].loc[sym, 'id'],
                                       weight=weight,
                                       volatility=idata[0].loc[sym, sym]) for sym, weight in weights.items()]
                PortfolioItem.objects.bulk_create(items)
                portfolio.stdev = stdev
                portfolio.er = er
                portfolio.save()
            except Unsatisfiable:
                # TODO: Return a message to the user that because they didn't make an initial deposit, we couldn't
                # come up with an appropriate portfolio, and they need to make a deposit to get started.
                logger.exception("No suitable portfolio could be found. Leaving empty.")

        return goal


class GoalUpdateSerializer(serializers.ModelSerializer):
    """
    For write (PUT/...) requests only
    """
    class Meta:
        model = Goal
        fields = (
            'name',
            'type',
            'portfolio_set',
        )  # list fields explicitly

    def __init__(self, *args, **kwargs):
        kwargs.pop('partial', None)
        super(GoalUpdateSerializer, self).__init__(*args, partial=True, **kwargs)

        # request based validation
        request = self.context.get('request')
        if not request:
            return # for swagger's dummy calls only

        #user = request.user

        # experimental / for advisors only
        #if user.is_advisor:
        #    self.fields['account'].queryset = \
        #        self.fields['account'].queryset.filter_by_advisor(user.advisor)


class GoalGoalTypeListSerializer(serializers.ModelSerializer):
    """
    Experimental
    For read (GET) requests only
    """
    class Meta:
        model = GoalTypes


class GoalPositionListSerializer(serializers.ModelSerializer):
    """
    Experimental
    For read (GET) requests only
    """
    class Meta:
        model = Position
