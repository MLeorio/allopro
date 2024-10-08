# Generated by Django 5.1 on 2024-09-03 18:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_category_options_alter_customer_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artisan',
            name='note',
            field=models.FloatField(blank=True, null=True, verbose_name="Moyenne des notes de l'artisan"),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.FloatField(blank=True, null=True, verbose_name="Note de l'artisan")),
                ('comment', models.CharField(blank=True, max_length=255, null=True, verbose_name="Commentaire sur l'artisan")),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de derniere modification')),
                ('artisan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.artisan')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.customer')),
            ],
            options={
                'verbose_name': 'Commentaire & Note',
                'verbose_name_plural': 'Commentaires & Notes',
            },
        ),
    ]
