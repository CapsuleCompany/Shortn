# Generated by Django 5.1.6 on 2025-02-13 23:44

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Shorten", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shortenedurl",
            name="ip_address",
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="shortenedurl",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
