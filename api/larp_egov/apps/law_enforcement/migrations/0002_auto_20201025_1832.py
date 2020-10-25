# Generated by Django 3.0.7 on 2020-10-25 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('law_enforcement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='misconductreport',
            name='penalty_status',
            field=models.IntegerField(choices=[(0, 'Penalty open'), (1, 'Penalty is active'), (2, 'Penalty is paid'), (3, 'Closed without payment')], default=0),
        ),
    ]