# Generated by Django 2.2.2 on 2019-06-16 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0007_auto_20190616_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trouble',
            name='create_time',
            field=models.DateTimeField(auto_now=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='trouble',
            name='process_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='处理时间'),
        ),
    ]