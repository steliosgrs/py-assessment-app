# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
import os, json
from pathlib import Path
import streamlit as st

from shared.course_loader import get_test_file_for_exercise
from shared.exercise_runner import test_exercise


# # Authenticate to firebase
# # @st.cache_resource
# def db_init():
#     # db = firestore.Client.from_service_account_json("firebase-credentials.json")
#     # Certification
#     cred = credentials.Certificate("firebase-credentials.json")

#     try:
#         firebase_admin.get_app()
#     except ValueError:
#         firebase_admin.initialize_app(cred)

#     # Database reference
#     db = firestore.client()
#     return db


# # @st.cache_resource
# def initialize_firebase():
#     """
#     Initialize Firebase Admin SDK using credentials from environment variable or file.
#     """
#     cred_path = os.environ.get("FIREBASE_CREDENTIALS", "firebase-credentials.json")

#     # Check if Firebase Admin is already initialized
#     if not firebase_admin._apps:
#         # If credentials are provided as an environment variable (JSON string)
#         if os.environ.get("FIREBASE_CREDENTIALS"):
#             cred_dict = json.loads(os.environ.get("FIREBASE_CREDENTIALS", "{}"))
#             cred = credentials.Certificate(cred_dict)
#             try:
#                 firebase_admin.initialize_app(cred)
#             except Exception as e:
#                 print(
#                     f"Error initializing Firebase Admin from environment variable: {e}"
#                 )
#                 return False
#         # If credentials are provided as a file
#         elif os.path.exists(cred_path):
#             cred = credentials.Certificate(cred_path)
#             try:
#                 firebase_admin.initialize_app(cred)
#             except Exception as e:
#                 print(f"Error initializing Firebase Admin from file: {e}")
#                 return False
#         else:
#             print(f"Firebase credentials not found at {cred_path}")
#             return False

#     return True


# # @st.cache_data
# def get_collection(db):
#     doc_ref = db.collection("modules").document("makhs")

#     # Then get the data at that reference.
#     doc = doc_ref.get()

#     # docs: StreamGenerator = col.stream()
#     return doc


# # db = db_init()
# db = initialize_firebase()
# print(db)
# # doc = get_collection(db)
# # Let's see what we got!
# # st.write("The id is: ", doc.id)
# # st.write("The contents are: ", doc.to_dict())

st.write("Or upload your solution file:")
uploaded_file = st.file_uploader("Choose a Python file", type=["py"])

# Submit button
submit_button = st.button("Submit & Test")


def save_code_to_temp_file(code: str, filename: str = "exercise.py") -> str:
    """
    Save code to a temporary file.

    Args:
        code (str): Python code to save
        filename (str): Name for the file

    Returns:
        str: Path to the temporary file
    """
    print("code", type(code))
    # Create a temporary directory
    Path("temp").mkdir(parents=True, exist_ok=True)
    temp_dir = Path("temp")
    file_path = os.path.join(temp_dir, filename)
    print(f"save_code_to_temp_file filename:  {file_path}")

    # Write code to the file
    with open(file_path, "w") as f:
        f.write(code)
    return file_path


if submit_button:
    # Determine which code to test
    if uploaded_file is not None:
        # Use uploaded file content
        exercise_content = uploaded_file.getvalue()
        print(exercise_content)
        exercise_code = exercise_content.decode("utf-8")
        print(exercise_code)
        save_code_to_temp_file(exercise_code)
    # else:
    # Use code from text editor
    # exercise_content = user_code.encode("utf-8")

    # Get test file for this exercise
    # test_success, test_message, test_content = get_test_file_for_exercise(exercise_id)

    # # Run tests
    # success, messages = test_exercise(exercise_content)
