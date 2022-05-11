# Generated by Django 4.0.4 on 2022-05-11 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idea',
            name='category',
        ),
        migrations.AddField(
            model_name='idea',
            name='category',
            field=models.ManyToManyField(related_name='ideas', to='idea.category'),
        ),
    ]
