# Generated by Django 4.0.4 on 2022-05-11 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Requester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('I', 'Investor'), ('B', 'Buyer'), ('C', 'Customer')], max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('status', models.CharField(choices=[('P', 'Pending'), ('R', 'Rejected'), ('A', 'Approved')], default='P', max_length=1)),
                ('chat_id', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ideas', to='idea.category')),
                ('requester', models.ManyToManyField(blank=True, to='idea.requester')),
            ],
        ),
    ]
