# Generated by Django 3.2 on 2021-05-01 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0002_rename_category_item_claims'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='link',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
