from django.conf import settings
import uuid

def upload_file_to_firebase(file, file_name):
    bucket = settings.FIREBASE_BUCKET
    blob = bucket.blob(f"{uuid.uuid4()}-{file_name}")
    blob.upload_from_file(file)
    blob.make_public()
    return blob.public_url
