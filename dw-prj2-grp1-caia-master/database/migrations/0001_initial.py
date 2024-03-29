# Generated by Django 3.1.2 on 2020-12-27 02:49

import database.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modification_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(default='images/avatar.png', upload_to='profile_pics')),
                ('account_cost', models.DecimalField(decimal_places=2, default=1000, max_digits=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item_name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(default=None, upload_to=database.models.user_directory_path)),
                ('votes', models.IntegerField(default=0)),
                ('flags', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_text', models.TextField(max_length=1000)),
                ('entry_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.customer')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.blog')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.customer')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.item')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerFlag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.customer')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.item')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(max_length=1000)),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.customer')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.item')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='database.customer'),
        ),
    ]
