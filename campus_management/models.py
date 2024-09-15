from django.db import models
import uuid

# Create your models here.

class Level(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Chapter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    levels = models.ManyToManyField(Level)

    def __str__(self):
        return self.name

class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    icon = models.URLField()
    chapters = models.ManyToManyField(Chapter)

    def __str__(self):
        return self.name

class Campus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    icon = models.URLField()
    description = models.TextField()
    subjects = models.ManyToManyField(Subject)

    class Meta:
        verbose_name_plural = "Campuses"

    def __str__(self):
        return self.name

class FileUpload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.CharField(max_length=255)
    file_url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
