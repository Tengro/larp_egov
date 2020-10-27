# Generated by Django 3.0.7 on 2020-10-27 19:27

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('law_enforcement', '0003_auto_20201026_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='misconductreport',
            name='misconduct_id',
            field=django_extensions.db.fields.RandomCharField(blank=True, editable=False, include_alpha=False, length=10, null=True, unique=True),
        ),
    ]