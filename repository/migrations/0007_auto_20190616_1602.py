# Generated by Django 2.2.2 on 2019-06-16 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0006_auto_20190616_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trouble',
            name='create_time',
            field=models.DateTimeField(verbose_name='创建时间'),
        ),
    ]
