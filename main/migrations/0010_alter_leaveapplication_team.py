# Generated by Django 4.1.7 on 2023-04-21 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_leaveapplication_applied_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaveapplication',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.team'),
        ),
    ]