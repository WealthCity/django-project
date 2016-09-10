import datetime

from django import test

from api.v1.tests.factories import GoalFactory, TransactionFactory, TickerFactory, PositionFactory
from main.models import Transaction, ExecutionDistribution, Execution, MarketOrderRequest
from portfolios.management.commands.providers.execution_providers.execution_provider_django import \
    ExecutionProviderDjango


class DjangoExecutionProviderTest(test.TestCase):
    def test_get_asset_weights_held_less_than1y(self):
        fund = TickerFactory.create(unit_price=2.1)
        goal = GoalFactory.create()
        today = datetime.date(2016, 1, 1)
        # Create a 6 month old execution, transaction and a distribution that caused the transaction
        order = MarketOrderRequest.objects.create(state=MarketOrderRequest.State.COMPLETE.value, account=goal.account)
        exec = Execution.objects.create(asset=fund,
                                        volume=10,
                                        order=order,
                                        price=2,
                                        executed=datetime.date(2015, 6, 1),
                                        amount=20)
        t1 = TransactionFactory.create(reason=Transaction.REASON_EXECUTION,
                                       to_goal=None,
                                       from_goal=goal,
                                       status=Transaction.STATUS_EXECUTED,
                                       executed=datetime.date(2015, 6, 1),
                                       amount=20)
        dist = ExecutionDistribution.objects.create(execution=exec, transaction=t1, volume=10)
        PositionFactory.create(goal=goal, ticker=fund, share=10)

        ep = ExecutionProviderDjango()
        vals = ep.get_asset_weights_held_less_than1y(goal, today)
        self.assertAlmostEqual(vals[fund.id], 21/goal.available_balance)