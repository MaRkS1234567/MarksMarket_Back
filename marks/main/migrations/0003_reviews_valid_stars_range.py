# Generated by Django 4.0.4 on 2022-04-17 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_reviews_options_reviews_stars_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='reviews',
            constraint=models.CheckConstraint(check=models.Q(('stars__gt', 0), ('stars__lt', 6)), name='valid_stars_range'),
        ),
    ]