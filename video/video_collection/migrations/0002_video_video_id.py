# Generated by Django 4.2 on 2023-05-01 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_collection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_id',
            field=models.CharField(default=0, max_length=40, unique=True),
            preserve_default=False,
        ),
    ]
