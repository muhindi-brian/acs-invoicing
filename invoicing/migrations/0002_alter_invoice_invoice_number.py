# Generated by Django 5.0.1 on 2024-01-04 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(editable=False, max_length=20, unique=True),
        ),
    ]
