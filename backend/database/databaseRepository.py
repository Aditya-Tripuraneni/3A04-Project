import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get the Firebase credentials path from the environment variable
firebase_credential_path = os.environ.get("FIREBASE_APPLICATION_CREDENTIALS")
if not firebase_credential_path or not os.path.exists(firebase_credential_path):
    raise FileNotFoundError("Firebase credentials file not found. Ensure FIREBASE_APPLICATION_CREDENTIALS is set correctly.")

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credential_path)
    firebase_admin.initialize_app(cred)
    logger.info("Firebase app initialized successfully")

# Create Firestore client
db = firestore.client()