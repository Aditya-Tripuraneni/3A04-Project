import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get the Firebase credentials JSON from the environment variable
firebase_credentials_json = os.environ.get("FIREBASE_APPLICATION_CREDENTIALS")
if not firebase_credentials_json:
    raise ValueError("FIREBASE_APPLICATION_CREDENTIALS environment variable is not set")

try:
    # Parse the JSON string into a dictionary
    service_account_info = json.loads(firebase_credentials_json)
except json.JSONDecodeError as e:
    raise ValueError("Invalid JSON in FIREBASE_APPLICATION_CREDENTIALS environment variable") from e

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred)
    logger.info("Firebase app initialized successfully")

# Create Firestore client
db = firestore.client()