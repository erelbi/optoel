# Generated by Django 2.2.22 on 2021-05-29 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_remove_valf_govde_govde_kurlenme_parti_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='valf_govde',
            name='govde_kurlenme_parti_no',
            field=models.PositiveIntegerField(null=True),
        ),
    ]