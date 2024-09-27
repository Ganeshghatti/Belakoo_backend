from django.urls import path
from . import views

urlpatterns = [
    path('campuses/', views.CampusListView.as_view(), name='campus-list'),
    path('campuses/<uuid:campus_id>/', views.CampusDetailView.as_view(), name='campus-detail'),
    path('subjects/<uuid:subject_id>/', views.SubjectDetailView.as_view(), name='subject-detail'),
    path('grades/<uuid:grade_id>/', views.GradeDetailView.as_view(), name='grade-detail'),
    path('chapters/<uuid:chapter_id>/lessons/', views.ChapterLessonsView.as_view(), name='chapter-lessons'),
    path('lessons/<str:lesson_code>/', views.LessonDetailView.as_view(), name='lesson-detail'),
    path('lessons/<uuid:lesson_id>/mark-done/', views.MarkLessonDoneView.as_view(), name='mark-lesson-done'),
    path('lessons/<uuid:lesson_id>/mark-not-done/', views.MarkLessonNotDoneView.as_view(), name='mark-lesson-not-done'),
    path('test', views.TestView.as_view(), name='test'),
]