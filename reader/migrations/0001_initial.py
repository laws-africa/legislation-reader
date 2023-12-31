# Generated by Django 3.2 on 2023-11-10 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frbr_uri', models.CharField(max_length=512, unique=True)),
                ('title', models.CharField(max_length=512)),
                ('metadata', models.JSONField()),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Expression',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frbr_uri', models.CharField(max_length=512, unique=True)),
                ('title', models.CharField(max_length=512)),
                ('language_code', models.CharField(max_length=3)),
                ('date', models.DateField()),
                ('content', models.TextField(blank=True, null=True)),
                ('toc_json', models.JSONField()),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='expressions', to='reader.work')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
