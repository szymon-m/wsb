# Generated by Django 2.2.1 on 2019-06-01 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uzytkownik', '0002_auto_20190601_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userid',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]