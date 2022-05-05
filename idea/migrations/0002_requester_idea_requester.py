# Generated by Django 4.0.4 on 2022-05-05 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('I', 'Investor'), ('B', 'Buyer'), ('C', 'Customer')], max_length=5)),
            ],
        ),
        migrations.AddField(
            model_name='idea',
            name='requester',
            field=models.ManyToManyField(blank=True, to='idea.requester'),
        ),
    ]