# Generated by Django 5.0.1 on 2024-01-06 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0006_alter_invoice_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
    ]
