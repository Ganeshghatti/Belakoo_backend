from django.db import models
import uuid

class Level(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    pdflink = models.URLField()
    is_done = models.BooleanField(default=False)

class Chapter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    levels = models.ManyToManyField(Level, related_name='chapters')

    def __str__(self):
        return self.name

class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    icon = models.URLField()
    chapters = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

class Campus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    icon = models.URLField()
    description = models.TextField()
    subjects = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='campuses')

    class Meta:
        verbose_name_plural = "Campuses"

    def __str__(self):
        return self.name
