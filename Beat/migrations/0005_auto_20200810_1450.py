# Generated by Django 3.0.7 on 2020-08-10 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Beat', '0004_auto_20200810_1448'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beat',
            old_name='category',
            new_name='bpm',
        ),
    ]
