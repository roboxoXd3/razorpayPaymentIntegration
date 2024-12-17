# Generated by Django 5.1.4 on 2024-12-17 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255, verbose_name='Order ID')),
                ('payment_id', models.CharField(max_length=255, verbose_name='Payment ID')),
                ('signature', models.CharField(max_length=255, verbose_name='Signature')),
                ('amount', models.IntegerField(verbose_name='Amount')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
