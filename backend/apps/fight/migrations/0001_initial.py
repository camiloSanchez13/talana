# Generated by Django 3.1.2 on 2022-10-27 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('character', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateTimeField(auto_now_add=True)),
                ('date_finish', models.DateTimeField(auto_now=True, null=True)),
                ('character_p1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characterp1', to='character.character')),
                ('character_p2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characterp2', to='character.character')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winnerpl', to='character.character')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movement', models.CharField(blank=True, max_length=4, null=True)),
                ('turn', models.PositiveIntegerField()),
                ('hit', models.CharField(blank=True, max_length=1, null=True)),
                ('fight_mov', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='fight.fight')),
            ],
        ),
    ]