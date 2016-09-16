# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0012_auto_20160917_0449'),
        ('main', '0054_auto_20160917_0623'),
    ]

    operations = [
        migrations.CreateModel(
            name='RetirementLifestyle',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('cost', models.PositiveIntegerField(help_text="The expected cost in system currency of this lifestyle in today's dollars")),
                ('holidays', models.TextField(help_text='The text for the holidays block')),
                ('eating_out', models.TextField(help_text='The text for the eating out block')),
                ('health', models.TextField(help_text='The text for the health block')),
                ('interests', models.TextField(help_text='The text for the interests block')),
                ('leisure', models.TextField(help_text='The text for the leisure block')),
                ('default_volunteer_days', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(7)], help_text='The default number of volunteer work days selected for this lifestyle')),
                ('default_paid_days', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(7)], help_text='The default number of paid work days selected for this lifestyle')),
            ],
        ),
        migrations.CreateModel(
            name='RetirementPlan',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True, null=True)),
                ('lifestyle', models.PositiveIntegerField(default=1, choices=[(1, 'Doing OK'), (2, 'Comfortable'), (3, 'Doing Well'), (4, 'Luxury')], help_text='The desired retirement lifestyle')),
                ('desired_income', models.PositiveIntegerField(help_text='The desired annual household pre-tax retirement income in system currency')),
                ('income', models.PositiveIntegerField(help_text='The current annual household pre-tax income at the start of your plan')),
                ('volunteer_days', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(7)], help_text='The number of volunteer work days selected')),
                ('paid_days', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(7)], help_text='The number of paid work days selected')),
                ('same_home', models.BooleanField(help_text='Will you be retiring in the same home?')),
                ('retirement_postal_code', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.MaxLengthValidator(10)], help_text='What postal code will you retire in?')),
                ('reverse_mortgage', models.BooleanField(help_text='Would you consider a reverse mortgage? (optional)')),
                ('retirement_home_style', models.PositiveIntegerField(choices=[(1, 'Single, Detached'), (2, 'Single, Attached'), (3, 'Multi-Unit, 9 or less'), (4, 'Multi-Unit, 10 - 20'), (5, 'Multi-Unit, 20+'), (6, 'Mobile Home'), (7, 'RV, Van, Boat, etc')], blank=True, null=True, help_text='The style of your retirement home')),
                ('retirement_home_price', models.PositiveIntegerField(blank=True, null=True, help_text="The price of your future retirement home (in today's dollars)")),
                ('beta_partner', models.BooleanField(default=False, help_text="Will BetaSmartz manage your partner's retirement assets as well?")),
                ('expenses', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of expenses [{id, desc, cat, who, amt},...]')),
                ('savings', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of savings [{id, desc, cat, who, amt},...]')),
                ('initial_deposits', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of deposits [{id, desc, cat, who, amt},...]')),
                ('income_growth', models.FloatField(default=0, help_text='Above consumer price index (inflation)')),
                ('expected_return_confidence', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('retirement_age', models.PositiveIntegerField()),
                ('btc', models.PositiveIntegerField(help_text='Before-tax annual income')),
                ('atc', models.PositiveIntegerField(help_text='After-tax annual income')),
                ('max_employer_match_percent', models.FloatField(blank=True, null=True, help_text='The percent the employer matches of before-tax contributions')),
                ('desired_risk', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], help_text='The selected risk appetite for this retirement plan')),
                ('recommended_risk', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], help_text='The calculated recommended risk for this retirement plan')),
                ('max_risk', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], help_text='The maximum allowable risk appetite for this retirement plan, based on our risk model')),
                ('calculated_life_expectancy', models.PositiveIntegerField()),
                ('selected_life_expectancy', models.PositiveIntegerField()),
                ('agreed_on', models.DateTimeField(blank=True, null=True)),
                ('portfolio', jsonfield.fields.JSONField(blank=True, null=True)),
                ('partner_data', jsonfield.fields.JSONField(blank=True, null=True)),
                ('client', models.ForeignKey(to='client.Client')),
                ('partner_plan', models.OneToOneField(to='retiresmartz.RetirementPlan', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partner_plan_reverse')),
            ],
        ),
        migrations.CreateModel(
            name='RetirementSpendingGoal',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('goal', models.OneToOneField(to='main.Goal', related_name='retirement_plan')),
                ('plan', models.ForeignKey(related_name='retirement_goals', to='retiresmartz.RetirementPlan')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='retirementplan',
            unique_together=set([('name', 'client')]),
        ),
    ]
