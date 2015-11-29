# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.contrib.auth.models
import django.core.validators
import django.utils.timezone
import django_localflavor_au.models
import main.fields
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('is_superuser', models.BooleanField(
                    help_text='Designates that this user has all permissions without explicitly assigning them.',
                    verbose_name='superuser status', default=False)),
                ('first_name', models.CharField(verbose_name='first name', max_length=30)),
                ('middle_name', models.CharField(verbose_name='middle name', max_length=30, blank=True)),
                ('last_name', models.CharField(verbose_name='last name', max_length=30)),
                ('username', models.CharField(editable=False, max_length=30, default='')),
                ('email', models.EmailField(unique=True, verbose_name='email address',
                                            error_messages={'unique': 'A user with that email already exists.'},
                                            max_length=254)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.',
                                                 verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(
                    help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                    verbose_name='active', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AccountGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Advisor',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('is_accepted', models.BooleanField(editable=False, default=False)),
                ('confirmation_key', models.CharField(editable=False, max_length=36, blank=True, null=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('date_of_birth', models.DateField(verbose_name='Date of birth')),
                ('gender',
                 models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=20, default='Male')),
                ('address_line_1', models.CharField(max_length=255)),
                ('address_line_2', models.CharField(max_length=255, blank=True, null=True)),
                ('city', models.CharField(max_length=255)),
                ('state', django_localflavor_au.models.AUStateField(
                    choices=[('ACT', 'Australian Capital Territory'), ('NSW', 'New South Wales'),
                             ('NT', 'Northern Territory'), ('QLD', 'Queensland'), ('SA', 'South Australia'),
                             ('TAS', 'Tasmania'), ('VIC', 'Victoria'), ('WA', 'Western Australia')], max_length=3)),
                ('post_code', django_localflavor_au.models.AUPostCodeField(max_length=4)),
                ('phone_number', django_localflavor_au.models.AUPhoneNumberField(max_length=10)),
                ('security_question_1', models.CharField(choices=[
                    ('What was the name of your elementary school?', 'What was the name of your elementary school?'), (
                    'What was the name of your favorite childhood friend?',
                    'What was the name of your favorite childhood friend?'),
                    ('What was the name of your childhood pet?', 'What was the name of your childhood pet?')],
                                                         max_length=255)),
                ('security_question_2', models.CharField(choices=[
                    ('What street did you live on in third grade?', 'What street did you live on in third grade?'),
                    ("What is your oldest sibling's birth month?", "What is your oldest sibling's birth month?"),
                    ('In what city did your mother and father meet?', 'In what city did your mother and father meet?')],
                                                         max_length=255)),
                ('security_answer_1', models.CharField(verbose_name='Answer', max_length=255)),
                ('security_answer_2', models.CharField(verbose_name='Answer', max_length=255)),
                ('medicare_number', models.CharField(max_length=50)),
                ('token', models.CharField(editable=False, max_length=36, null=True)),
                ('letter_of_authority', models.FileField(upload_to='')),
                ('work_phone', django_localflavor_au.models.AUPhoneNumberField(max_length=10, null=True)),
                ('betasmartz_agreement', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AssetClass',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, validators=[
                    django.core.validators.RegexValidator(regex='^[0-9a-zA-Z_]+$',
                                                          message='Invalid character only accept (0-9a-zA-Z_) ')])),
                ('display_order', models.PositiveIntegerField()),
                ('primary_color', main.fields.ColorField(max_length=10)),
                ('foreground_color', main.fields.ColorField(max_length=10)),
                ('drift_color', main.fields.ColorField(max_length=10)),
                ('asset_class_explanation', models.TextField(blank=True, default='')),
                ('tickers_explanation', models.TextField(blank=True, default='')),
                ('display_name', models.CharField(max_length=255)),
                ('investment_type',
                 models.CharField(choices=[('BONDS', 'BONDS'), ('STOCKS', 'STOCKS')], max_length=255)),
                ('super_asset_class', models.CharField(
                    choices=[('EQUITY_AU', 'EQUITY_AU'), ('EQUITY_US', 'EQUITY_US'), ('EQUITY_EU', 'EQUITY_EU'),
                             ('EQUITY_EM', 'EQUITY_EM'), ('EQUITY_INT', 'EQUITY_INT'), ('EQUITY_UK', 'EQUITY_UK'),
                             ('EQUITY_JAPAN', 'EQUITY_JAPAN'), ('EQUITY_AS', 'EQUITY_AS'), ('EQUITY_CN', 'EQUITY_CN'),
                             ('FIXED_INCOME_AU', 'FIXED_INCOME_AU'), ('FIXED_INCOME_US', 'FIXED_INCOME_US'),
                             ('FIXED_INCOME_EU', 'FIXED_INCOME_EU'), ('FIXED_INCOME_EM', 'FIXED_INCOME_EM'),
                             ('FIXED_INCOME_INT', 'FIXED_INCOME_INT'), ('FIXED_INCOME_UK', 'FIXED_INCOME_UK'),
                             ('FIXED_INCOME_JAPAN', 'FIXED_INCOME_JAPAN'), ('FIXED_INCOME_AS', 'FIXED_INCOME_AS'),
                             ('FIXED_INCOME_CN', 'FIXED_INCOME_CN')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='AuthorisedRepresentative',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('is_accepted', models.BooleanField(editable=False, default=False)),
                ('confirmation_key', models.CharField(editable=False, max_length=36, blank=True, null=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('date_of_birth', models.DateField(verbose_name='Date of birth')),
                ('gender',
                 models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=20, default='Male')),
                ('address_line_1', models.CharField(max_length=255)),
                ('address_line_2', models.CharField(max_length=255, blank=True, null=True)),
                ('city', models.CharField(max_length=255)),
                ('state', django_localflavor_au.models.AUStateField(
                    choices=[('ACT', 'Australian Capital Territory'), ('NSW', 'New South Wales'),
                             ('NT', 'Northern Territory'), ('QLD', 'Queensland'), ('SA', 'South Australia'),
                             ('TAS', 'Tasmania'), ('VIC', 'Victoria'), ('WA', 'Western Australia')], max_length=3)),
                ('post_code', django_localflavor_au.models.AUPostCodeField(max_length=4)),
                ('phone_number', django_localflavor_au.models.AUPhoneNumberField(max_length=10)),
                ('security_question_1', models.CharField(choices=[
                    ('What was the name of your elementary school?', 'What was the name of your elementary school?'), (
                    'What was the name of your favorite childhood friend?',
                    'What was the name of your favorite childhood friend?'),
                    ('What was the name of your childhood pet?', 'What was the name of your childhood pet?')],
                                                         max_length=255)),
                ('security_question_2', models.CharField(choices=[
                    ('What street did you live on in third grade?', 'What street did you live on in third grade?'),
                    ("What is your oldest sibling's birth month?", "What is your oldest sibling's birth month?"),
                    ('In what city did your mother and father meet?', 'In what city did your mother and father meet?')],
                                                         max_length=255)),
                ('security_answer_1', models.CharField(verbose_name='Answer', max_length=255)),
                ('security_answer_2', models.CharField(verbose_name='Answer', max_length=255)),
                ('medicare_number', models.CharField(max_length=50)),
                ('letter_of_authority', models.FileField(upload_to='')),
                ('betasmartz_agreement', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AutomaticDeposit',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('frequency', models.CharField(
                    choices=[('MONTHLY', '1/mo'), ('TWICE_A_MONTH', '2/mo'), ('EVERY_OTHER_WEEK', '2/mo'),
                             ('WEEKLY', 'WEEKLY')], max_length=50)),
                ('enabled', models.BooleanField(default=True)),
                ('amount', models.FloatField()),
                ('transaction_date_time_1', models.DateTimeField(null=True)),
                ('transaction_date_time_2', models.DateTimeField(null=True)),
                ('last_plan_change', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AutomaticWithdrawal',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('frequency', models.CharField(
                    choices=[('MONTHLY', '1/mo'), ('TWICE_A_MONTH', '2/mo'), ('EVERY_OTHER_WEEK', '2/mo'),
                             ('WEEKLY', 'WEEKLY')], max_length=50)),
                ('enabled', models.BooleanField(default=True)),
                ('amount', models.FloatField()),
                ('transaction_date_time_1', models.DateTimeField(null=True)),
                ('transaction_date_time_2', models.DateTimeField(null=True)),
                ('last_plan_change', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('is_accepted', models.BooleanField(editable=False, default=False)),
                ('confirmation_key', models.CharField(editable=False, max_length=36, blank=True, null=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('date_of_birth', models.DateField(verbose_name='Date of birth')),
                ('gender',
                 models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=20, default='Male')),
                ('address_line_1', models.CharField(max_length=255)),
                ('address_line_2', models.CharField(max_length=255, blank=True, null=True)),
                ('city', models.CharField(max_length=255)),
                ('state', django_localflavor_au.models.AUStateField(
                    choices=[('ACT', 'Australian Capital Territory'), ('NSW', 'New South Wales'),
                             ('NT', 'Northern Territory'), ('QLD', 'Queensland'), ('SA', 'South Australia'),
                             ('TAS', 'Tasmania'), ('VIC', 'Victoria'), ('WA', 'Western Australia')], max_length=3)),
                ('post_code', django_localflavor_au.models.AUPostCodeField(max_length=4)),
                ('phone_number', django_localflavor_au.models.AUPhoneNumberField(max_length=10)),
                ('security_question_1', models.CharField(choices=[
                    ('What was the name of your elementary school?', 'What was the name of your elementary school?'), (
                    'What was the name of your favorite childhood friend?',
                    'What was the name of your favorite childhood friend?'),
                    ('What was the name of your childhood pet?', 'What was the name of your childhood pet?')],
                                                         max_length=255)),
                ('security_question_2', models.CharField(choices=[
                    ('What street did you live on in third grade?', 'What street did you live on in third grade?'),
                    ("What is your oldest sibling's birth month?", "What is your oldest sibling's birth month?"),
                    ('In what city did your mother and father meet?', 'In what city did your mother and father meet?')],
                                                         max_length=255)),
                ('security_answer_1', models.CharField(verbose_name='Answer', max_length=255)),
                ('security_answer_2', models.CharField(verbose_name='Answer', max_length=255)),
                ('medicare_number', models.CharField(max_length=50)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('client_agreement', models.FileField(upload_to='')),
                ('tax_file_number', models.CharField(max_length=50, blank=True, null=True)),
                ('provide_tfn', models.IntegerField(
                    choices=[(0, 'Yes'), (1, 'I am a non-resident of Australia'), (2, 'I want to claim an exemption'),
                             (3, 'I do not want to quote a Tax File Number or exemption')], verbose_name='Provide TFN?',
                    default=0)),
                ('associated_to_broker_dealer', models.BooleanField(choices=[(False, 'No'), (True, 'Yes')],
                                                                    verbose_name='You are employed by or associated with a broker dealer.',
                                                                    default=False)),
                ('ten_percent_insider', models.BooleanField(choices=[(False, 'No'), (True, 'Yes')],
                                                            verbose_name='You are a 10% shareholder, director, or policy maker of a publicly traded company.',
                                                            default=False)),
                ('public_position_insider', models.BooleanField(choices=[(False, 'No'), (True, 'Yes')],
                                                                verbose_name='Do you or a family member hold a public office position.',
                                                                default=False)),
                ('us_citizen', models.BooleanField(choices=[(False, 'No'), (True, 'Yes')],
                                                   verbose_name='Are you a US citizen/person for the purpose of US Federal Income Tax.',
                                                   default=False)),
                ('employment_status', models.CharField(
                    choices=[('FULL_TIME', 'Employed (full-time)'), ('PART_TIME', 'Employed (part-time)'),
                             ('SELF_EMPLOYED', 'Self-employed'), ('STUDENT', 'Student'), ('RETIRED', 'Retired'),
                             ('HOMEMAKER', 'Homemaker'), ('UNEMPLOYED', 'Not employed')], max_length=20)),
                ('net_worth', models.FloatField(default=0)),
                ('income', models.FloatField(default=0)),
                ('occupation', models.CharField(max_length=255, blank=True, null=True)),
                ('employer', models.CharField(max_length=255, blank=True, null=True)),
                ('betasmartz_agreement', models.BooleanField()),
                ('advisor_agreement', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClientAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('custom_fee', models.PositiveIntegerField(default=0)),
                ('account_type',
                 models.CharField(choices=[('PERSONAL', 'Personal Account')], max_length=20, default='PERSONAL')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CostOfLivingIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('state', django_localflavor_au.models.AUStateField(
                    choices=[('ACT', 'Australian Capital Territory'), ('NSW', 'New South Wales'),
                             ('NT', 'Northern Territory'), ('QLD', 'Queensland'), ('SA', 'South Australia'),
                             ('TAS', 'Tasmania'), ('VIC', 'Victoria'), ('WA', 'Western Australia')], unique=True,
                    max_length=3)),
                ('value', models.FloatField(default=80.99)),
            ],
        ),
        migrations.CreateModel(
            name='DataApiDict',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('api', models.CharField(choices=[('YAHOO', 'YAHOO'), ('GOOGLE', 'GOOGLE')], max_length=50)),
                ('platform_symbol', models.CharField(max_length=20)),
                ('api_symbol', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='EmailInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('inviter_id', models.PositiveIntegerField()),
                ('send_date', models.DateTimeField(auto_now=True)),
                ('send_count', models.PositiveIntegerField(default=0)),
                ('status',
                 models.PositiveIntegerField(choices=[(0, 'Pending'), (1, 'Submitted'), (3, 'Active'), (4, 'Closed')],
                                             default=0)),
                ('invitation_type', models.PositiveIntegerField(
                    choices=[(0, 'Advisor'), (1, 'Authorised representative'), (3, 'Client'), (2, 'Supervisor')],
                    default=3)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('other_retirement_income_cents', models.FloatField(default=0)),
                ('complete', models.BooleanField(default=False)),
                ('retirement_zip', django_localflavor_au.models.AUPostCodeField(max_length=4)),
                ('income_replacement_ratio', models.FloatField(null=True)),
                ('retirement_age', models.PositiveIntegerField(null=True)),
                ('spouse_retirement_age', models.PositiveIntegerField(null=True)),
                ('desired_retirement_income_cents', models.FloatField(default=0)),
                ('savings_advice_chance', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialPlanAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('annual_contribution_cents', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialPlanExternalAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('account_type', models.CharField(max_length=100)),
                ('balance_cents', models.FloatField(default=0, null=True)),
                ('annual_contribution_cents', models.FloatField(default=0, null=True)),
                ('account_owner', models.CharField(max_length=100, null=True)),
                ('institution_name', models.CharField(max_length=255, null=True)),
                ('investment_type', models.CharField(max_length=100, null=True)),
                ('advisor_fee_percent', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('complete', models.BooleanField(default=False)),
                ('marital_status', models.CharField(max_length=100, default='single')),
                ('retired', models.BooleanField(default=False)),
                ('life_expectancy', models.FloatField(default=70, null=True)),
                ('pretax_income_cents', models.FloatField(default=0, null=True)),
                ('social_security_monthly_amount_cents', models.FloatField(default=0, null=True)),
                ('expected_inflation', models.FloatField(default=2.5)),
                ('social_security_percent_expected', models.FloatField(default=0, null=True)),
                ('annual_salary_percent_growth', models.FloatField(default=0, null=True)),
                ('average_tax_percent', models.FloatField(default=0, null=True)),
                ('spouse_name', models.CharField(max_length=100, null=True)),
                ('spouse_estimated_birthdate', models.DateTimeField(null=True)),
                ('spouse_retired', models.BooleanField(default=False)),
                ('spouse_life_expectancy', models.FloatField(default=80, null=True)),
                ('spouse_pretax_income_cents', models.FloatField(default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Firm',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('dealer_group_number', models.CharField(max_length=50, blank=True, null=True)),
                ('slug', models.CharField(unique=True, editable=False, max_length=100)),
                ('logo_url', models.ImageField(verbose_name='White logo', upload_to='', blank=True, null=True)),
                ('knocked_out_logo_url',
                 models.ImageField(verbose_name='Colored logo', upload_to='', blank=True, null=True)),
                ('client_agreement_url',
                 models.FileField(verbose_name='Client Agreement (PDF)', upload_to='', blank=True, null=True)),
                ('form_adv_part2_url', models.FileField(verbose_name='Form Adv', upload_to='', blank=True, null=True)),
                ('token', models.CharField(editable=False, max_length=36)),
                ('fee', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FirmData',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('afsl_asic', models.CharField(verbose_name='AFSL/ASIC number', max_length=50)),
                ('afsl_asic_document', models.FileField(verbose_name='AFSL/ASIC doc.', upload_to='')),
                ('office_address_line_1', models.CharField(verbose_name='Office address 1', max_length=255)),
                ('office_address_line_2',
                 models.CharField(verbose_name='Office address 2', max_length=255, blank=True, null=True)),
                ('office_state', django_localflavor_au.models.AUStateField(
                    choices=[('ACT', 'Australian Capital Territory'), ('NSW', 'New South Wales'),
                             ('NT', 'Northern Territory'), ('QLD', 'Queensland'), ('SA', 'South Australia'),
                             ('TAS', 'Tasmania'), ('VIC', 'Victoria'), ('WA', 'Western Australia')], max_length=3)),
                ('office_city', models.CharField(max_length=255)),
                ('office_post_code', django_localflavor_au.models.AUPostCodeField(max_length=4)),
                ('postal_address_line_1', models.CharField(verbose_name='Postal address 1', max_length=255)),
                ('postal_address_line_2',
                 models.CharField(verbose_name='Postal address 2', max_length=255, blank=True, null=True)),
                ('postal_state', django_localflavor_au.models.AUStateField(
                    choices=[('ACT', 'Australian Capital Territory'), ('NSW', 'New South Wales'),
                             ('NT', 'Northern Territory'), ('QLD', 'Queensland'), ('SA', 'South Australia'),
                             ('TAS', 'Tasmania'), ('VIC', 'Victoria'), ('WA', 'Western Australia')], max_length=3)),
                ('same_address', models.BooleanField(default=False)),
                ('postal_city', models.CharField(max_length=255)),
                ('postal_post_code', django_localflavor_au.models.AUPostCodeField(max_length=4)),
                ('daytime_phone_number', django_localflavor_au.models.AUPhoneNumberField(max_length=10)),
                ('mobile_phone_number', django_localflavor_au.models.AUPhoneNumberField(max_length=10)),
                ('fax_number', django_localflavor_au.models.AUPhoneNumberField(max_length=10)),
                ('alternate_email_address',
                 models.EmailField(verbose_name='Email address', max_length=254, blank=True, null=True)),
                ('last_change', models.DateField(auto_now=True)),
                ('fee_bank_account_name', models.CharField(verbose_name='Name', max_length=100)),
                ('fee_bank_account_branch_name', models.CharField(verbose_name='Branch name', max_length=100)),
                ('fee_bank_account_bsb_number', models.CharField(verbose_name='BSB number', max_length=20)),
                ('fee_bank_account_number', models.CharField(verbose_name='Account number', max_length=20)),
                ('fee_bank_account_holder_name', models.CharField(verbose_name='Account holder', max_length=100)),
                ('australian_business_number', models.CharField(verbose_name='ABN', max_length=20)),
            ],
            options={
                'verbose_name': 'Firm detail',
            },
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('target', models.FloatField(default=0)),
                ('income', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('completion_date', models.DateTimeField()),
                ('allocation', models.FloatField()),
                ('account_type', models.CharField(max_length=20, default='INVESTING')),
                ('type', models.CharField(max_length=20, default='RETIREMENT')),
                ('drift', models.FloatField(default=0)),
                ('total_balance_db', models.FloatField(verbose_name='total balance', default=0)),
                ('portfolios', models.TextField(null=True)),
                ('au_size', models.FloatField(default=0)),
                ('au_allocation', models.FloatField(default=0)),
                ('au_currency_hedge', models.BooleanField(default=False)),
                ('dm_size', models.FloatField(default=0)),
                ('dm_allocation', models.FloatField(default=0)),
                ('dm_currency_hedge', models.BooleanField(default=False)),
                ('usa_size', models.FloatField(default=0)),
                ('usa_allocation', models.FloatField(default=0)),
                ('usa_currency_hedge', models.BooleanField(default=False)),
                ('uk_size', models.FloatField(default=0)),
                ('uk_allocation', models.FloatField(default=0)),
                ('uk_currency_hedge', models.BooleanField(default=False)),
                ('europe_size', models.FloatField(default=0)),
                ('europe_allocation', models.FloatField(default=0)),
                ('europe_currency_hedge', models.BooleanField(default=False)),
                ('japan_size', models.FloatField(default=0)),
                ('japan_allocation', models.FloatField(default=0)),
                ('japan_currency_hedge', models.BooleanField(default=False)),
                ('asia_size', models.FloatField(default=0)),
                ('asia_allocation', models.FloatField(default=0)),
                ('asia_currency_hedge', models.BooleanField(default=False)),
                ('china_size', models.FloatField(default=0)),
                ('china_allocation', models.FloatField(default=0)),
                ('china_currency_hedge', models.BooleanField(default=False)),
                ('em_size', models.FloatField(default=0)),
                ('em_allocation', models.FloatField(default=0)),
                ('em_currency_hedge', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MonthlyPrices',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('symbol', models.CharField(max_length=100)),
                ('price', models.FloatField(default=0)),
                ('date', models.DateTimeField()),
            ],
            options={
                'ordering': ['symbol', 'date'],
            },
        ),
        migrations.CreateModel(
            name='Performer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('symbol', models.CharField(max_length=20, blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('group', models.CharField(
                    choices=[('STRATEGY', 'STRATEGY'), ('BENCHMARK', 'BENCHMARK'), ('BOND', 'BOND'),
                             ('STOCK', 'STOCK')], max_length=20, default='BENCHMARK')),
                ('allocation', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('fee', models.PositiveIntegerField(default=0)),
                ('api',
                 models.CharField(choices=[('YAHOO', 'YAHOO'), ('GOOGLE', 'GOOGLE')], max_length=20, default='YAHOO')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('share', models.FloatField()),
                ('goal', models.ForeignKey(related_name='positions', to='main.Goal')),
            ],
        ),
        migrations.CreateModel(
            name='SymbolReturnHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('return_number', models.FloatField(default=0)),
                ('symbol', models.CharField(max_length=20)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('symbol', models.CharField(max_length=10, validators=[
                    django.core.validators.RegexValidator(regex='^[^ ]+$', message='Invalid symbol format')])),
                ('display_name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('ordering', models.IntegerField(blank=True, default='')),
                ('url', models.URLField()),
                ('unit_price', models.FloatField(default=10)),
                ('currency', models.CharField(max_length=10, default='AUD')),
                ('asset_class', models.ForeignKey(related_name='tickers', to='main.AssetClass')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('type', models.CharField(
                    choices=[('REBALANCE', 'REBALANCE'), ('ALLOCATION', 'ALLOCATION'), ('DEPOSIT', 'DEPOSIT'),
                             ('WITHDRAWAL', 'WITHDRAWAL'), ('MARKET_CHANGE', 'MARKET_CHANGE')], max_length=20)),
                ('amount', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('EXECUTED', 'EXECUTED')], max_length=20,
                                            default='PENDING')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('executed_date', models.DateTimeField(null=True)),
                ('new_balance', models.FloatField(default=0)),
                ('inversion', models.FloatField(default=0)),
                ('return_fraction', models.FloatField(default=0)),
                ('account', models.ForeignKey(related_name='transactions', to='main.Goal')),
                ('from_account',
                 models.ForeignKey(to='main.ClientAccount', blank=True, null=True, related_name='transactions_from')),
                ('to_account',
                 models.ForeignKey(to='main.ClientAccount', blank=True, null=True, related_name='transactions_to')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionMemo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('category', models.CharField(max_length=255)),
                ('comment', models.TextField()),
                ('transaction_type', models.CharField(max_length=20)),
                ('transaction', models.ForeignKey(related_name='memos', to='main.Transaction')),
            ],
        ),
        migrations.AddField(
            model_name='position',
            name='ticker',
            field=models.ForeignKey(to='main.Ticker'),
        ),
    ]
