# Generated by Django 4.0.4 on 2022-05-11 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('idea', '0003_remove_idea_category_idea_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ideas', to='user.user'),
        ),
    ]
