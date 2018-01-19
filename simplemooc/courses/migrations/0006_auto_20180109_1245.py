# Generated by Django 2.0 on 2018-01-09 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20180105_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='announcement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='courses.Announcement', verbose_name='Anúncio'),
        ),
    ]
