# Generated by Django 5.0.7 on 2024-11-22 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myauth", "0002_alter_profile_first_name_alter_profile_last_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="bio",
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
