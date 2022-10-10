# Generated by Django 3.2.14 on 2022-08-04 07:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("financial", "0007_auto_20220804_1136"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payhistory",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pays",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
