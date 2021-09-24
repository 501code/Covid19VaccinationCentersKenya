# Generated by Django 2.2 on 2021-09-24 20:06

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210914_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='VaccineCenterFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('waiting_time', models.IntegerField(default=1)),
                ('vaccine_available', models.BooleanField(default=True)),
                ('vaccines', models.CharField(blank=True, max_length=255, null=True)),
                ('vaccine_center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.VaccineCenter')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]