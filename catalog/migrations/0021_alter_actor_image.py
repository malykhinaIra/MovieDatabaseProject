# Generated by Django 4.0.2 on 2023-05-14 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_actor_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='image',
            field=models.ImageField(default=' ', upload_to='D:\\movie_database\\MovieDatabaseProject\\catalog\\static\\catalog\\img'),
        ),
    ]