# Generated by Django 3.1.7 on 2021-10-03 02:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('room_name', models.CharField(default='Default room name', max_length=255, null=True)),
            ],
        ),
    ]
