from django.db import models
import uuid
import json

class Campus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    icon = models.URLField()
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Campuses"

    def __str__(self):
        return self.name

class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    icon = models.URLField()
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

class Grade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')

    def __str__(self):
        return self.name

class Chapter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='chapters')

    def __str__(self):
        return self.name

class Level(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    pdflink = models.URLField()
    is_done = models.BooleanField(default=False)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='levels')

    def __str__(self):
        return self.name

class Lesson(models.Model):
    lesson_code = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    objective = models.TextField(null=True, blank=True)
    duration = models.CharField(max_length=50, null=True, blank=True)
    specific_learning_outcome = models.TextField(null=True, blank=True)
    behavioural_outcome = models.TextField(null=True, blank=True)
    materials_required = models.TextField(null=True, blank=True)
    activate = models.JSONField(null=True, blank=True)
    acquire = models.JSONField(null=True, blank=True)
    apply = models.JSONField(null=True, blank=True)
    assess = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.lesson_code

    def set_activate(self, data):
        self.activate = json.dumps(data)

    def get_activate(self):
        return json.loads(self.activate) if self.activate else {}

    def set_acquire(self, data):
        self.acquire = json.dumps(data)

    def get_acquire(self):
        return json.loads(self.acquire) if self.acquire else {}

    def set_apply(self, data):
        self.apply = json.dumps(data)

    def get_apply(self):
        return json.loads(self.apply) if self.apply else {}

    def set_assess(self, data):
        self.assess = json.dumps(data)

    def get_assess(self):
        return json.loads(self.assess) if self.assess else {}
