# Generated by Django 5.1 on 2024-10-02 16:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LeaveApplication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "leave_type",
                    models.CharField(
                        choices=[
                            ("casual", "Casual Leave"),
                            ("compensatory", "Compensatory Leave"),
                            ("emergency", "Emergency Leave"),
                            ("marriage", "Marriage Leave"),
                            ("maternity", "Maternity Leave"),
                            ("paternity", "Paternity Leave"),
                            ("sick", "Sick Leave"),
                            ("study", "Study Leave"),
                            ("unpaid", "Unpaid Leave"),
                        ],
                        max_length=50,
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="attachments/")),
                (
                    "leave_application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attachments",
                        to="LeaveApp.leaveapplication",
                    ),
                ),
            ],
        ),
    ]
