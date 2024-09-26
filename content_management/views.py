from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Campus, Subject, Grade, Chapter, Level, Lesson
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
import pandas as pd
import math

class TestView(APIView):
    def get(self, request):
        try:
            file_path = 'Belakoo_backend/content/sample.xlsx'
            df = pd.read_excel(file_path)
            
            # Function to find a keyword and its value
            def find_keyword_value(keyword):
                for i, row in df.iterrows():
                    if keyword in row.values:
                        col_index = row.tolist().index(keyword)
                        if col_index + 1 < len(row):
                            return row[col_index + 1]
                return None

            # List of keywords to search for
            keywords = [
                'LESSON CODE', 'SUBJECT', 'OBJECTIVE', 'Duration',
                'Specific Learning Outcome', 'Behavioural Outcome',
                'Materials Required', 'HOOK', 'ASSESS', 'INFORM','ENGAGE','TEACH','GUIDED PRACTICE','INDEPENDENT PRACTICE','SHARE','ASSESSMENT'
            ]

            # Extract values for each keyword
            lesson_data = {}
            for keyword in keywords:
                value = find_keyword_value(keyword)
                if value is not None:
                    lesson_data[keyword] = value

            # Print extracted data for debugging
            print("Extracted data:", lesson_data)

            return Response(lesson_data)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return Response({"error": str(e)}, status=500)

class CampusListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        campuses = Campus.objects.all()
        data = [{
            'id': str(campus.id),
            'name': campus.name,
            'icon': campus.icon,
            'description': campus.description,
        } for campus in campuses]
        return Response(data)

class CampusDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, campus_id):
        try:
            campus = Campus.objects.get(id=campus_id)
            data = {
                'id': str(campus.id),
                'name': campus.name,
                'icon': campus.icon,
                'description': campus.description,
                'subjects': [{
                    'id': str(subject.id),
                    'name': subject.name,
                    'icon': subject.icon,
                } for subject in campus.subjects.all()]
            }
            return Response(data)
        except Campus.DoesNotExist:
            return Response({'error': 'Campus not found'}, status=status.HTTP_404_NOT_FOUND)

class SubjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_id):
        try:
            subject = Subject.objects.get(id=subject_id)
            data = {
                'id': str(subject.id),
                'name': subject.name,
                'icon': subject.icon,
                'grades': [{
                    'id': str(grade.id),
                    'name': grade.name,
                } for grade in subject.grades.all()]
            }
            return Response(data)
        except Subject.DoesNotExist:
            return Response({'error': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)

class GradeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, grade_id):
        try:
            grade = Grade.objects.get(id=grade_id)
            data = {
                'id': str(grade.id),
                'name': grade.name,
                'chapters': [{
                    'id': str(chapter.id),
                    'name': chapter.name,
                    'levels': [{
                        'id': str(level.id),
                        'name': level.name,
                        'pdflink': level.pdflink,
                        'is_done': level.is_done
                    } for level in chapter.levels.all()]
                } for chapter in grade.chapters.all()]
            }
            return Response(data)
        except Grade.DoesNotExist:
            return Response({'error': 'Grade not found'}, status=status.HTTP_404_NOT_FOUND)

class ChapterLevelsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chapter_id):
        try:
            chapter = Chapter.objects.get(id=chapter_id)
            levels = chapter.levels.all()
            data = {
                'chapter_id': str(chapter.id),
                'chapter_name': chapter.name,
                'levels': [{
                    'id': str(level.id),
                    'name': level.name,
                    'pdflink': level.pdflink,
                    'is_done': level.is_done
                } for level in levels]
            }
            return Response(data)
        except Chapter.DoesNotExist:
            return Response({'error': 'Chapter not found'}, status=status.HTTP_404_NOT_FOUND)

class MarkLevelDoneView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, level_id):
        try:
            level = Level.objects.get(id=level_id)
            level.is_done = True
            level.save()
            return Response({'message': 'Level marked as done'}, status=status.HTTP_200_OK)
        except Level.DoesNotExist:
            return Response({'error': 'Level not found'}, status=status.HTTP_404_NOT_FOUND)

class MarkLevelNotDoneView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, level_id):
        try:
            level = Level.objects.get(id=level_id)
            level.is_done = False
            level.save()
            return Response({'message': 'Level marked as not done'}, status=status.HTTP_200_OK)
        except Level.DoesNotExist:
            return Response({'error': 'Level not found'}, status=status.HTTP_404_NOT_FOUND)