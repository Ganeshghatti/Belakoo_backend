from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Campus, Subject, Grade, Proficiency, Lesson
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
import pandas as pd
import math

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
                'proficiencies': [{
                    'id': str(proficiency.id),
                    'name': proficiency.name,
                    'lessons': [{
                        'id': str(lesson.id),
                        'name': lesson.name,
                        'lesson_code': lesson.lesson_code,
                        'is_done': lesson.is_done
                    } for lesson in proficiency.lessons.all()]
                } for proficiency in grade.proficiencies.all()]
            }
            return Response(data)
        except Grade.DoesNotExist:
            return Response({'error': 'Grade not found'}, status=status.HTTP_404_NOT_FOUND)

class ProficiencyLessonsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, proficiency_id):
        try:
            proficiency = Proficiency.objects.get(id=proficiency_id)
            lessons = proficiency.lessons.all()
            data = {
                'proficiency_id': str(proficiency.id),
                'proficiency_name': proficiency.name,
                'lessons': [{
                    'id': str(lesson.id),
                    'lesson_code': lesson.lesson_code,
                    'name': lesson.name,
                    'is_done': lesson.is_done
                } for lesson in lessons]
            }
            return Response(data)
        except Proficiency.DoesNotExist:
            return Response({'error': 'Proficiency not found'}, status=status.HTTP_404_NOT_FOUND)

class LessonDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, lesson_code):
        try:
            lesson = Lesson.objects.get(lesson_code=lesson_code)
            data = {
                'id': str(lesson.id),
                'lesson_code': lesson.lesson_code,
                'name': lesson.name,
                'subject': lesson.subject.name,
                'grade': lesson.grade.name,
                'proficiency': lesson.proficiency.name,
                'is_done': lesson.is_done,
                'objective': lesson.objective,
                'duration': lesson.duration,
                'specific_learning_outcome': lesson.specific_learning_outcome,
                'behavioural_outcome': lesson.behavioural_outcome,
                'materials_required': lesson.materials_required,
                'activate': lesson.activate,
                'acquire': lesson.acquire,
                'apply': lesson.apply,
                'assess': lesson.assess,
            }
            return Response(data)
        except Lesson.DoesNotExist:
            return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)

class MarkLessonDoneView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_id):
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            lesson.is_done = True
            lesson.save()
            return Response({'message': 'Lesson marked as done'}, status=status.HTTP_200_OK)
        except Lesson.DoesNotExist:
            return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)

class MarkLessonNotDoneView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_id):
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            lesson.is_done = False
            lesson.save()
            return Response({'message': 'Lesson marked as not done'}, status=status.HTTP_200_OK)
        except Lesson.DoesNotExist:
            return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)

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
                'Specific Learning Outcome ', 'Behavioural Outcome',
                'Materials Required', 'HOOK', 'ASSESS', 'INFORM','ENGAGE','TEACH','GUIDED PRACTICE','INDEPENDENT PRACTICE','SHARE','ASSESSMENT'
            ]

            # Extract values for each keyword
            lesson_data = {}
            for keyword in keywords:
                value = find_keyword_value(keyword)
                if value is not None:
                    lesson_data[keyword] = value

            # Print extracted data for debugging
            extracted_code = lesson_data['LESSON CODE'].split()[0]

            subject_code = extracted_code.split('.')[0]
            grade_code = extracted_code.split('.')[1]
            proficiency_code = extracted_code.split('.')[2]
            lesson_number = extracted_code.split('.')[3]

            subject = Subject.objects.get(subject_code=subject_code)
            grade = Grade.objects.get(grade_code=grade_code, subject=subject)
            proficiency = Proficiency.objects.get(proficiency_code=proficiency_code, grade=grade)

            # Create and save the Lesson object
            lesson = Lesson.objects.create(
                lesson_code=extracted_code,
                name=f"Lesson {lesson_number}",
                subject=subject,
                grade=grade,
                proficiency=proficiency,
                objective=lesson_data.get('OBJECTIVE'),
                duration=lesson_data.get('Duration'),
                specific_learning_outcome=lesson_data.get('Specific Learning Outcome'),
                behavioural_outcome=lesson_data.get('Behavioural Outcome'),
                materials_required=lesson_data.get('Materials Required'),
                activate={"HOOK": lesson_data.get('HOOK')},
                acquire={"INFORM": lesson_data.get('INFORM'), "ENGAGE": lesson_data.get('ENGAGE'), "TEACH": lesson_data.get('TEACH')},
                apply={"GUIDED PRACTICE": lesson_data.get('GUIDED PRACTICE'), "INDEPENDENT PRACTICE": lesson_data.get('INDEPENDENT PRACTICE'), "SHARE": lesson_data.get('SHARE')},
                assess={"ASSESSMENT": lesson_data.get('ASSESS')}
            )
            print(lesson)
            return Response({"message": "Lesson created successfully", "lesson_id": str(lesson.id)})

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return Response({"error": str(e)}, status=500)
