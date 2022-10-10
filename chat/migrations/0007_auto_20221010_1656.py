# Generated by Django 3.2.14 on 2022-10-10 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_auto_20221002_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='chat_image/'),
        ),
        migrations.AlterField(
            model_name='message',
            name='voice',
            field=models.FileField(blank=True, null=True, upload_to='chat_voice/'),
        ),
    ]