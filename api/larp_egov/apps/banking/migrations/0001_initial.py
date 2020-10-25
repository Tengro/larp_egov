# Generated by Django 3.0.7 on 2020-10-25 21:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankSubscription',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('title', models.CharField(max_length=512)),
                ('description', models.TextField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=1, max_digits=12, null=True)),
                ('is_governmental_tax', models.BooleanField(default=False)),
                ('extraction_period', models.IntegerField(choices=[(6, 'Once per six hours'), (12, 'Once per twelve hours'), (24, 'Once per 24 hours')], default=24)),
                ('limited_approval', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Corporation',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('title', models.CharField(max_length=512)),
                ('linked_account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CorporationMembership',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('status', models.IntegerField(choices=[(1, 'Plain membership'), (2, 'Membership with funds access'), (3, 'Membership with funds & '), (4, 'Excecutive (funds, list of members)')], default=1)),
                ('corporation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banking.Corporation')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='corporation',
            name='members',
            field=models.ManyToManyField(related_name='corporate_membership', through='banking.CorporationMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='BankUserSubscriptionIntermediary',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('is_approved', models.BooleanField(default=True)),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banking.BankSubscription')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BankTransaction',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('amount', models.DecimalField(decimal_places=1, max_digits=12, null=True)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('is_finished', models.BooleanField(default=False)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('time_finished', models.DateTimeField(null=True)),
                ('comment', models.CharField(blank=True, max_length=512, null=True)),
                ('reciever', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recieved_transactions', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='banksubscription',
            name='subscribers',
            field=models.ManyToManyField(related_name='subscriptions', through='banking.BankUserSubscriptionIntermediary', to=settings.AUTH_USER_MODEL),
        ),
    ]
