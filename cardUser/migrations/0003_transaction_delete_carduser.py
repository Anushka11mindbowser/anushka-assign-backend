# Generated by Django 4.0.4 on 2022-08-04 13:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cardUser', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=255, null=True)),
                ('customer_email', models.CharField(default='anushkapawar35@gmail.com', max_length=255, null=True)),
                ('product_name', models.CharField(max_length=255, null=True)),
                ('total_amount', models.IntegerField(null=True)),
                ('payment_method', models.CharField(max_length=255, null=True)),
                ('order_created', models.DateTimeField(default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='CardUser',
        ),
    ]
