# Generated by Django 3.2.7 on 2021-09-17 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_book_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='book_count',
            field=models.IntegerField(),
        ),
    ]
