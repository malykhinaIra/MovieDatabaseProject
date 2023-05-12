# Generated by Django 4.0.2 on 2023-04-15 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_alter_movie_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='review',
        ),
        migrations.AddField(
            model_name='review',
            name='movie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.movie'),
        ),
    ]