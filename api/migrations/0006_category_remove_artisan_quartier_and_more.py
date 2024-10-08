# Generated by Django 5.1 on 2024-08-30 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_user_otp_alter_user_otp_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_category', models.CharField(max_length=100, unique=True, verbose_name='Libellé de la catégorie')),
                ('description_category', models.CharField(max_length=255, verbose_name='Description de la catégorie')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de Modification')),
            ],
        ),
        migrations.RemoveField(
            model_name='artisan',
            name='quartier',
        ),
        migrations.RemoveField(
            model_name='artisan',
            name='workshop_name',
        ),
        migrations.AddField(
            model_name='artisan',
            name='note',
            field=models.FloatField(null=True, verbose_name="Note de l'artisan"),
        ),
        migrations.AlterField(
            model_name='artisan',
            name='metier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.metier'),
        ),
        migrations.CreateModel(
            name='Atelier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_atelier', models.CharField(max_length=255, verbose_name="Nom de l'atelier")),
                ('quartier', models.CharField(max_length=255, verbose_name='Quartier')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de Modification')),
                ('artisan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.artisan')),
            ],
        ),
        migrations.AddField(
            model_name='metier',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.category'),
        ),
    ]
