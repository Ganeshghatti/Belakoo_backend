from django.contrib import admin
from .models import Campus, Subject, Chapter, Level

# Register models directly without custom admin classes
admin.site.register(Campus)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(Level)
