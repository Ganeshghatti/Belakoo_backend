from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Campus, Subject, Chapter, Level
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

class CampusListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        campuses = Campus.objects.all()
        data = [{
            'id': campus.id,
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
                'id': campus.id,
                'name': campus.name,
                'icon': campus.icon,
                'description': campus.description,
                'subjects': [{
                    'id': subject.id,
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
                'id': subject.id,
                'name': subject.name,
                'icon': subject.icon,
                'chapters': [{
                    'id': chapter.id,
                    'name': chapter.name,
                    'levels': [{
                        'id': level.id,
                        'name': level.name,
                        'link': level.link,
                        'is_done': level.is_done
                    } for level in chapter.levels.all()]
                } for chapter in subject.chapters.all()]
            }
            return Response(data)
        except Subject.DoesNotExist:
            return Response({'error': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)
