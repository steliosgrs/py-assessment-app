# # test_import.py at project root
# import sys
# from shared.firebase import get_exercises_by_module, get_all_modules

# print("Import successful!")
# print(f"get_exercises_by_module: {get_exercises_by_module}")
# print(f"get_all_modules: {get_all_modules}")


from firebase_admin import db, credentials, initialize_app

# Authenticate to firebase

cred = credentials.Certificate("firebase-credentials.json")
initialize_app(credential=cred,{"databaseURL": })