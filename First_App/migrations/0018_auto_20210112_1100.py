# Generated by Django 3.1.5 on 2021-01-12 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('First_App', '0017_auto_20210109_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='courses',
            field=models.ManyToManyField(blank=True, to='First_App.Course'),
        ),
    ]