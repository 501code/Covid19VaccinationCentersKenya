# Generated by Django 2.2 on 2021-05-11 17:14

from django.db import migrations
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='county',
            name='location',
            field=location_field.models.plain.PlainLocationField(default=1, max_length=63),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subcounty',
            name='location',
            field=location_field.models.plain.PlainLocationField(default=1, max_length=63),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vaccinecenter',
            name='location',
            field=location_field.models.plain.PlainLocationField(default=1, max_length=63),
            preserve_default=False,
        ),
    ]
