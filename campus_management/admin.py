from django.contrib import admin
from .models import Campus, Subject, Chapter, Level
from .utils import upload_file_to_firebase

class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')
    
    def save_model(self, request, obj, form, change):
        file = request.FILES.get('file')
        if file:
            file_url = upload_file_to_firebase(file, file.name)
            obj.link = file_url
        super().save_model(request, obj, form, change)

admin.site.register(Campus)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(Level, LevelAdmin)
