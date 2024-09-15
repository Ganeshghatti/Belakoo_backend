from django.urls import path
from . import views

urlpatterns = [
    path('campuses/', views.CampusListView.as_view(), name='campus-list'),
    path('campuses/<uuid:campus_id>/', views.CampusDetailView.as_view(), name='campus-detail'),
    path('subjects/<uuid:subject_id>/', views.SubjectDetailView.as_view(), name='subject-detail'),
    path('upload/', views.FileUploadView.as_view(), name='file-upload'),
]
