# Generated by Django 4.0.3 on 2023-01-20 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_remove_game_radius_game_zoom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cache',
            name='latitude',
            field=models.DecimalField(decimal_places=8, max_digits=10),
        ),
        migrations.AlterField(
            model_name='cache',
            name='longitude',
            field=models.DecimalField(decimal_places=8, max_digits=10),
        ),
        migrations.AlterField(
            model_name='game',
            name='latitude',
            field=models.DecimalField(decimal_places=8, max_digits=10),
        ),
        migrations.AlterField(
            model_name='game',
            name='longitude',
            field=models.DecimalField(decimal_places=8, max_digits=10),
        ),
    ]