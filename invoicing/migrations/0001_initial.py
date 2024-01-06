# Generated by Django 5.0.1 on 2024-01-04 12:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='AFRICA CALLING SAFARIS LTD', max_length=100)),
                ('logo_url', models.URLField(default='https://example.com/default-logo.png')),
                ('address', models.TextField(default='P.O. Box 12237-00100, Nairobi, Kenya.')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField()),
                ('due_date', models.DateField()),
                ('invoice_number', models.CharField(max_length=20, unique=True)),
                ('trip_name', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('trip_description', models.TextField()),
                ('quantity', models.PositiveIntegerField()),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(choices=[('KES', 'Kenyan Shilling'), ('USD', 'US Dollar'), ('EUR', 'Euro')], default='KES', max_length=3)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('prepared_by', models.CharField(max_length=100)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoicing.client')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoicing.company')),
            ],
        ),
    ]