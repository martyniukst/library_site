# Generated by Django 3.2.7 on 2021-09-17 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='book_count',
            field=models.IntegerField(default=1),
        ),
    ]