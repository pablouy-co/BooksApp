# Generated by Django 2.2.5 on 2020-03-27 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0025_auto_20200327_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='pub_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha de publicacion'),
        ),
    ]