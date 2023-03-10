# Generated by Django 4.1.5 on 2023-01-07 08:41

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name', max_length=100)),
                ('address', models.CharField(help_text='Address', max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated date')),
            ],
            options={
                'verbose_name': 'merchant point',
                'verbose_name_plural': 'merchant points',
            },
        ),
        migrations.CreateModel(
            name='Printer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name', max_length=100)),
                ('api_key', models.UUIDField(default=uuid.uuid4, help_text='API access key', unique=True)),
                ('check_type', models.CharField(choices=[('kitchen', 'Check for kitchen'), ('client', 'Check for client')], help_text='Type of check', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated date')),
                ('merchant_point', models.ForeignKey(help_text='Merchant point', on_delete=django.db.models.deletion.PROTECT, to='api.merchantpoint')),
            ],
            options={
                'verbose_name': 'printer',
                'verbose_name_plural': 'printers',
            },
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_type', models.CharField(choices=[('kitchen', 'Check for kitchen'), ('client', 'Check for client')], help_text='Type of check', max_length=10)),
                ('order', models.JSONField(help_text='Order data')),
                ('status', models.CharField(choices=[('new', 'New'), ('rendered', 'Rendered'), ('printed', 'Printed')], default='new', help_text='Status of check', max_length=10)),
                ('pdf_file', models.FileField(help_text='PDF file', null=True, upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated date')),
                ('printer', models.ForeignKey(help_text='Printer', on_delete=django.db.models.deletion.PROTECT, to='api.printer')),
            ],
            options={
                'verbose_name': 'check',
                'verbose_name_plural': 'checks',
            },
        ),
    ]
