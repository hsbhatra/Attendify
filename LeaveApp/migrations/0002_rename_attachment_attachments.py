# Generated by Django 5.1 on 2024-10-02 16:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("LeaveApp", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Attachment",
            new_name="Attachments",
        ),
    ]