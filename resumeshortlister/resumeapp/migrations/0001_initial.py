# Generated by Django 4.2.19 on 2025-03-11 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=20)),
                ('skills', models.TextField()),
                ('years', models.IntegerField()),
                ('is_duplicate', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='JobListing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('specifications', models.TextField(blank=True, null=True)),
                ('required_skills', models.ManyToManyField(to='resumeapp.skill')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('position', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100)),
                ('duration', models.CharField(max_length=50)),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experience', to='resumeapp.resume')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('degree', models.CharField(max_length=100)),
                ('field', models.CharField(max_length=100)),
                ('institution', models.CharField(max_length=200)),
                ('year', models.CharField(max_length=4)),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education', to='resumeapp.resume')),
            ],
        ),
    ]
