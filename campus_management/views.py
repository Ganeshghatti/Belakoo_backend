from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Campus, Subject, Chapter, FileUpload
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .utils import upload_file_to_firebase
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

class CampusListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        campuses = Campus.objects.all()
        data = []
        for campus in campuses:
            campus_data = {
                'id': campus.id,
                'name': campus.name,
                'icon': campus.icon,
                'description': campus.description,
            }
            data.append(campus_data)
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
                'subjects': []
            }
            for subject in campus.subjects.all():
                subject_data = {
                    'id': subject.id,
                    'name': subject.name,
                    'icon': subject.icon,
                }
                data['subjects'].append(subject_data)
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
                'chapters': []
            }
            for chapter in subject.chapters.all():
                chapter_data = {
                    'id': chapter.id,
                    'name': chapter.name,
                    'levels': []
                }
                for level in chapter.levels.all():
                    level_data = {
                        'id': level.id,
                        'name': level.name,
                        'link': level.link
                    }
                    chapter_data['levels'].append(level_data)
                data['chapters'].append(chapter_data)
            return Response(data)
        except Subject.DoesNotExist:
            return Response({'error': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)

class SomeUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')
        if file:
            file_url = upload_file_to_firebase(file, file.name)
            # Save file_url to your model or return it in the response
            return Response({'file_url': file_url}, status=status.HTTP_201_CREATED)
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.data['file']
        file_url = upload_file_to_firebase(file_obj, file_obj.name)
        
        # Save file information to the database
        file_upload = FileUpload.objects.create(
            file_name=file_obj.name,
            file_url=file_url
        )
        
        return Response({
            'file_url': file_url,
            'file_id': str(file_upload.id)
        }, status=status.HTTP_201_CREATED)
