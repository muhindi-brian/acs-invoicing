# Generated by Django 5.0.1 on 2024-01-06 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0005_invoice_number_of_days_alter_invoice_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]