# Generated by Django 2.2.2 on 2019-06-16 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0005_tpl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trouble',
            name='evaluate',
            field=models.IntegerField(choices=[(1, '不满意'), (2, '一般'), (3, '满意')], null=True),
        ),
    ]
