# Generated by Django 4.2.5 on 2023-09-27 20:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='Category name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Category description')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Name')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email address')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activity')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='Created')),
                ('sending_time', models.TimeField(default='00:00', verbose_name='Time of sending mailings')),
                ('frequency', models.CharField(choices=[('DAILY', 'Every day'), ('WEEKLY', 'Once a week'), ('MONTHLY', 'Once a month')], default='daily', max_length=50, verbose_name='Interval')),
                ('status', models.CharField(choices=[('FINISH', 'Finished'), ('CREATE', 'Created'), ('START', 'Started')], default='created', max_length=50, verbose_name='Status')),
                ('finish_date', models.DateField(default='2025-01-01', verbose_name='Termination date')),
                ('finish_time', models.TimeField(default='00:00', verbose_name='Termination time')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activity')),
                ('client', models.ManyToManyField(to='mailing.client', verbose_name='Client')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Mailing',
                'verbose_name_plural': 'Mailings',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=200, verbose_name='Topic')),
                ('message', models.TextField(verbose_name='Message body')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.category')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
        migrations.CreateModel(
            name='MessageVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_number', models.PositiveSmallIntegerField(verbose_name='Version number')),
                ('version_name', models.CharField(max_length=100, verbose_name='Version name')),
                ('is_active', models.BooleanField(verbose_name='Flag of the current version')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.message', verbose_name='Message')),
            ],
        ),
        migrations.CreateModel(
            name='MailingLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_try', models.DateTimeField(auto_now_add=True, verbose_name='The last attempt')),
                ('status', models.CharField(choices=[('ok', 'Success'), ('failed', 'Failure')], default='ok', max_length=30, verbose_name='Status')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.client', verbose_name='Client')),
                ('mail_settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing', verbose_name='Mailing')),
            ],
            options={
                'verbose_name': 'Mailing log',
                'verbose_name_plural': 'Mailing logs',
            },
        ),
        migrations.AddField(
            model_name='mailing',
            name='message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.message', verbose_name='Message'),
        ),
    ]
