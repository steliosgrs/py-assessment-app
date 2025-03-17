import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os, json
import streamlit as st


# Authenticate to firebase
@st.cache_resource
def db_init():
    # db = firestore.Client.from_service_account_json("firebase-credentials.json")
    # Certification
    cred = credentials.Certificate("firebase-credentials.json")

    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred)

    # Database reference
    db = firestore.client()
    return db


@st.cache_resource
def initialize_firebase():
    """
    Initialize Firebase Admin SDK using credentials from environment variable or file.
    """
    cred_path = os.environ.get("FIREBASE_CREDENTIALS", "firebase-credentials.json")

    # Check if Firebase Admin is already initialized
    if not firebase_admin._apps:
        # If credentials are provided as an environment variable (JSON string)
        if os.environ.get("FIREBASE_CREDENTIALS"):
            cred_dict = json.loads(os.environ.get("FIREBASE_CREDENTIALS", "{}"))
            cred = credentials.Certificate(cred_dict)
            try:
                firebase_admin.initialize_app(cred)
            except Exception as e:
                print(
                    f"Error initializing Firebase Admin from environment variable: {e}"
                )
                return False
        # If credentials are provided as a file
        elif os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            try:
                firebase_admin.initialize_app(cred)
            except Exception as e:
                print(f"Error initializing Firebase Admin from file: {e}")
                return False
        else:
            print(f"Firebase credentials not found at {cred_path}")
            return False

    return True


# @st.cache_data
def get_collection(db):
    doc_ref = db.collection("modules").document("makhs")

    # Then get the data at that reference.
    doc = doc_ref.get()

    # docs: StreamGenerator = col.stream()
    return doc


# db = db_init()
db = initialize_firebase()
print(db)
# doc = get_collection(db)
# Let's see what we got!
# st.write("The id is: ", doc.id)
# st.write("The contents are: ", doc.to_dict())
