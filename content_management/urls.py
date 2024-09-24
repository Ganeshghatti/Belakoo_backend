from django.urls import path
from . import views

urlpatterns = [
    path('campuses/', views.CampusListView.as_view(), name='campus-list'),
    path('campuses/<uuid:campus_id>/', views.CampusDetailView.as_view(), name='campus-detail'),
    path('subjects/<uuid:subject_id>/', views.SubjectDetailView.as_view(), name='subject-detail'),
    path('grades/<uuid:grade_id>/', views.GradeDetailView.as_view(), name='grade-detail'),
    path('chapters/<uuid:chapter_id>/levels/', views.ChapterLevelsView.as_view(), name='chapter-levels'),
    path('levels/<uuid:level_id>/mark-done/', views.MarkLevelDoneView.as_view(), name='mark-level-done'),
    path('levels/<uuid:level_id>/mark-not-done/', views.MarkLevelNotDoneView.as_view(), name='mark-level-not-done'),
]