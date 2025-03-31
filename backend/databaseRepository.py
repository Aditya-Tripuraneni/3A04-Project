import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os


firebase_credential_path = os.environ.get("FIREBASE_APPLICATION_CREDENTIALS")
print(firebase_credential_path)

if not firebase_credential_path or not os.path.exists(firebase_credential_path):
    raise FileNotFoundError("Firebase credentials file not found. Ensure FIREBASE_CREDENTIAL is set correctly.")

cred = credentials.Certificate(firebase_credential_path)
print(cred)
firebase_admin.initialize_app(cred)

print("Firebase app initialized successfully")
db = firestore.client()

