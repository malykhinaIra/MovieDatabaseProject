# Generated by Django 4.0.2 on 2023-05-14 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0024_alter_actor_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='cover_image',
            field=models.ImageField(default=' ', upload_to=''),
        ),
    ]