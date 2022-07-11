# Generated by Django 3.1.6 on 2021-04-15 12:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='cat_img',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='posts',
            name='related1',
            field=models.ManyToManyField(blank=True, related_name='_posts_related1_+', to='posts.Posts'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_img', models.FileField(upload_to='')),
                ('user_post', models.CharField(max_length=300)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='posts',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.userprofile'),
        ),
    ]