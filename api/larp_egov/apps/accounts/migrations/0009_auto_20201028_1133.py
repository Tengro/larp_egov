# Generated by Django 3.0.7 on 2020-10-28 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20201027_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='bank_account',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=12),
        ),
    ]
