# Generated by Django 2.2.22 on 2021-05-10 18:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0004_auto_20210509_1611'),
    ]

    operations = [
        migrations.RenameField(
            model_name='valf_test',
            old_name='kayit_tarihi',
            new_name='test_tarihi',
        ),
        migrations.RemoveField(
            model_name='valf_test',
            name='personel',
        ),
        migrations.RemoveField(
            model_name='valf_test',
            name='valf',
        ),
        migrations.AddField(
            model_name='valf_test',
            name='test_personel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='test_personel', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
