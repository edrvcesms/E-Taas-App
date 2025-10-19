import firebase_admin
from firebase_admin import credentials, auth, exceptions
import os

firebase_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
cred = credentials.Certificate(firebase_path)

if not firebase_admin._apps:
    firebase_admin.initialize_app(credential=cred)


def verify_firebase_token(id_token: str) -> dict | None:
    try:
        decoded_token = auth.verify_id_token(id_token)
        return {
            "email": decoded_token["email"],
            "uid": decoded_token["uid"],
        }
    except exceptions.FirebaseError as e:
        print("Firebase verification failed:", e)
        return None