# Generated by Django 5.1.1 on 2024-10-10 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_alter_subscription_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='stripe_product_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
