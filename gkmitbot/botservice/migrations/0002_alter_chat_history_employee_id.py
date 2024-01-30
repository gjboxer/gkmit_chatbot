# Generated by Django 4.2.9 on 2024-01-30 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("botservice", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chat_history",
            name="Employee_ID",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="botservice.employee",
            ),
        ),
    ]
