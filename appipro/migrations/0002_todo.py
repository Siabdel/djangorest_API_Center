# Generated by Django 2.2.13 on 2021-04-03 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appipro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Todo',
                'ordering': ('-created',),
            },
        ),
    ]
