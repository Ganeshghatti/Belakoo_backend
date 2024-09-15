# Generated by Django 5.1.1 on 2024-09-15 04:33

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campus_management', '0003_alter_campus_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=255)),
                ('file_url', models.URLField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]