import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("serviceAccountKey.json")
print(cred)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'belakoo-52465'
})

bucket = storage.bucket()
