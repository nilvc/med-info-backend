# Generated by Django 3.1.7 on 2021-10-20 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20211013_1458'),
        ('Rooms', '0003_invite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='invite_for',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile'),
        ),
        migrations.AlterField(
            model_name='invite',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Rooms.room'),
        ),
    ]
