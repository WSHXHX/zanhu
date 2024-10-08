# Generated by Django 5.0.7 on 2024-08-21 14:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='liked',
            field=models.ManyToManyField(related_name='liked_news', to=settings.AUTH_USER_MODEL, verbose_name='点赞用户'),
        ),
    ]
