# Generated by Django 5.0.1 on 2024-01-30 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('po_app', '0003_alter_stock_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockinbasket',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]
