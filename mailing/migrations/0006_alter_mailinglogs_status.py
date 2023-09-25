# Generated by Django 4.2.5 on 2023-09-25 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0005_alter_client_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailinglogs',
            name='status',
            field=models.CharField(choices=[('ok', 'Success'), ('failed', 'Failure')], default='ok', max_length=30, verbose_name='Status'),
        ),
    ]