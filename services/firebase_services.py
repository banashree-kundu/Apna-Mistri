import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
import os,json
from services import upload
from flask import jsonify
from datetime import datetime, timedelta
import pytz
firebase_creds = os.environ.get("FIREBASE_CONFIG")

if firebase_creds:
    cred_dict = json.loads(firebase_creds)
    cred = credentials.Certificate(cred_dict)
else:
    # fallback for local dev
    raise Exception("FIREBASE_SERVICE_ACCOUNT environment variable not set")

# ======================
# Firebase Init
# ======================

# Avoid 'app already exists' error if this file is imported more than once
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

