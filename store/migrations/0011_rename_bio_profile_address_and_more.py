# Generated by Django 5.1.2 on 2024-11-15 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_profile_delete_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='bio',
            new_name='address',
        ),
        migrations.AddField(
            model_name='profile',
            name='social_media_links',
            field=models.TextField(blank=True),
        ),
    ]
