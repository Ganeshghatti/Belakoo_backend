from django.contrib import admin
from .models import Campus, Subject, Grade, Chapter, Level

# Register models directly without custom admin classes
admin.site.register(Campus)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Chapter)
admin.site.register(Level)
