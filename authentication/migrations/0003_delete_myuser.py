# Generated by Django 3.1.1 on 2021-09-13 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_myuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]
