# Generated by Django 3.1.5 on 2021-02-27 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingtransactions',
            name='token',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
