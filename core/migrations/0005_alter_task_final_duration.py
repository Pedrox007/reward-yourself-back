# Generated by Django 4.2.2 on 2023-06-21 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_task_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='final_duration',
            field=models.DurationField(blank=True, null=True, verbose_name='Final Duration'),
        ),
    ]
