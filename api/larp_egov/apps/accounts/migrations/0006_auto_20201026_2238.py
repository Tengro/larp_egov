# Generated by Django 3.0.7 on 2020-10-26 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_useraccount_is_corporate_fiction_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='telegram_id',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
