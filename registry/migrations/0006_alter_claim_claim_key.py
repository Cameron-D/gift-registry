# Generated by Django 3.2 on 2021-05-02 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0005_auto_20210502_0535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='claim_key',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
