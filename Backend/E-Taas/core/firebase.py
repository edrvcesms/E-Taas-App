from firebase_admin import credentials, auth, initialize_app
from config import settings
from fastapi import Header, HTTPException

cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
initialize_app(cred)

async def verify_firebase_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    id_token = authorization.split(" ")[1]
    try:
        decoded = auth.verify_id_token(id_token)
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjlkMjEzMGZlZjAyNTg3ZmQ4ODYxODg2OTgyMjczNGVmNzZhMTExNjUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZS10YWFzLW1zbWUiLCJhdWQiOiJlLXRhYXMtbXNtZSIsImF1dGhfdGltZSI6MTc2MTE5MTY4NCwidXNlcl9pZCI6IjBDenBWZnZmZnZjdDZGY3Nub0hnSm9FQ1NWZDIiLCJzdWIiOiIwQ3pwVmZ2ZmZ2Y3Q2RmNzbm9IZ0pvRUNTVmQyIiwiaWF0IjoxNzYxMTkxNjg0LCJleHAiOjE3NjExOTUyODQsImVtYWlsIjoiZWRyaG92aWNlc21hc0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiZWRyaG92aWNlc21hc0BnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.YgUGPh5cn2GYotfLrK0npfu_MeCJDaLdKzDLHoarnXLzLgnTrxlPwt_Bfo_1nW5tGsjLXLL80BruUQxnJAxm1Hvae3Q6VxTt3M-VqMhBGKrCB_6IhQtD-0zJ7U3rXMlbX7OiAjDRmH2NMg5VAxk49sCjcZNvimM-6oat-ZD4Lws8D5X_2bWRDEOB6qhmggLVhtQwbqtvd-JMUGaqGkq4ViQYccf6l2Qa3670VpqwaK6-EGd9v30FFzq9eHdt-qmy2Xgu1zrLeJC3UUT7pSJ_AijAoFYHfRdRDHKNxTsGjHbWWan_R72uEhti1fllDLkvBXtfsTLEftccXJt5qlKRWA"

try:
    verify_firebase_token(authorization=f"Bearer {token}")
    print("Token is valid.")
except HTTPException as e:
    print(f"Token verification failed: {e.detail}")
