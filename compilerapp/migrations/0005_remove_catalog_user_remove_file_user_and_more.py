# Generated by Django 4.2 on 2023-05-09 11:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("compilerapp", "0004_catalog_user_file_user_section_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="catalog",
            name="user",
        ),
        migrations.RemoveField(
            model_name="file",
            name="user",
        ),
        migrations.RemoveField(
            model_name="section",
            name="user",
        ),
    ]
