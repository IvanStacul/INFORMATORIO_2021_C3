# Generated by Django 3.2.6 on 2021-09-02 22:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.player')),
            ],
        ),
    ]
