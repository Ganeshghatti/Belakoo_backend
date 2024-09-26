# Generated by Django 5.1.1 on 2024-09-26 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_management', '0002_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='assess',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='behavioural_outcome',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='duration',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='hook',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='inform',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='materials_required',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='objective',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='specific_learning_outcome',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='subject',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]