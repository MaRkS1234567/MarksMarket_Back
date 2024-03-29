# Generated by Django 4.2.dev20220902080224 on 2023-04-15 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_reviewofuser_reviewofuser_valid_rating_range'),
    ]

    operations = [
        migrations.CreateModel(
            name='Yield',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('description', models.TextField()),
                ('price', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to='products/')),
            ],
        ),
    ]
