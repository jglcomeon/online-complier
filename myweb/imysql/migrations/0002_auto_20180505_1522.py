# Generated by Django 2.0.3 on 2018-05-05 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imysql', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='anonymity',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='anonymity',
            field=models.CharField(max_length=10, null=True),
        ),
    ]