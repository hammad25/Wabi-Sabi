# Generated by Django 3.2.15 on 2022-09-24 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20220922_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='query_type',
            field=models.CharField(choices=[(0, 'Question'), (1, 'Contribute')], max_length=11),
        ),
    ]