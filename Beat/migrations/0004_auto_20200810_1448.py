# Generated by Django 3.0.7 on 2020-08-10 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Beat', '0003_auto_20200725_1617'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beat',
            name='created',
        ),
        migrations.AlterField(
            model_name='beat',
            name='category',
            field=models.CharField(blank=True, default='', max_length=5, null=True, verbose_name='BPM'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
