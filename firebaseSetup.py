import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("iqol-crm-firebase-adminsdk-fbsvc-19f803d1d1.json")
firebase_admin.initialize_app(cred)
# Firestore client
db = firestore.client()

def test_connection():
    # Example: read from a collection named "users"
    users_ref = db.collection("vaultUsers").stream()
    for user in users_ref:
        print(f"{user.id} => {user.to_dict()}")

if __name__ == "__main__":
    test_connection()
