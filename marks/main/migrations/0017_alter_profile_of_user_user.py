# Generated by Django 4.2.dev20220902080224 on 2023-04-28 04:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0016_alter_profile_of_user_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile_of_user',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
