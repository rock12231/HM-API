# Generated by Django 5.0.1 on 2024-02-05 21:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hackeathon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('registration_start_date', models.DateField()),
                ('registration_end_date', models.DateField()),
                ('registration_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('prize', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rules', models.TextField()),
                ('eligibility', models.TextField()),
                ('contact', models.TextField()),
                ('link', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='hackeathon/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dislikes', models.ManyToManyField(blank=True, related_name='hackeathon_dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='hackeathon_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dislikes', models.ManyToManyField(blank=True, related_name='comment_dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comments', models.ManyToManyField(blank=True, related_name='post_comments', to='API.usercomment')),
                ('dislikes', models.ManyToManyField(blank=True, related_name='post_dislikes', to=settings.AUTH_USER_MODEL)),
                ('intrested', models.ManyToManyField(blank=True, related_name='post_intrested', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='post_likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='usercomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.userpost'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('college', models.CharField(blank=True, max_length=100)),
                ('branch', models.CharField(blank=True, max_length=20)),
                ('year', models.CharField(blank=True, max_length=10)),
                ('batch', models.CharField(blank=True, max_length=10)),
                ('occupation', models.CharField(blank=True, choices=[('S', 'Student'), ('P', 'Professional')], max_length=1, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('githublink', models.TextField(blank=True)),
                ('linkedinlink', models.TextField(blank=True)),
                ('twitterlink', models.TextField(blank=True)),
                ('instagramlink', models.TextField(blank=True)),
                ('facebooklink', models.TextField(blank=True)),
                ('stackoverflowlink', models.TextField(blank=True)),
                ('otherlink', models.TextField(blank=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
