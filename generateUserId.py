import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin only once
if not firebase_admin._apps:
    cred = credentials.Certificate("iqol-crm-firebase-adminsdk-fbsvc-19f803d1d1.json")
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()


def generate_user_id() -> str:
    counter_ref = db.collection("vaultAdmin").document("lastUser")

    @firestore.transactional
    def transaction_op(transaction, counter_ref):
        counter_doc = counter_ref.get(transaction=transaction)

        count = 999  # fallback
        prefix = "A"
        label = "UID"

        if counter_doc.exists:
            data = counter_doc.to_dict()
            count = data.get("count", 999)
            prefix = data.get("prefix", "A")
            label = data.get("label", "UID")

        # Increment
        new_count = count + 1

        # Handle rollover
        if new_count > 9999:
            new_count = 1000
            if prefix == "Z":
                raise ValueError("User ID prefix limit reached (Z)")
            prefix = chr(ord(prefix) + 1)

        # Construct ID
        generated_user_id = f"{label}{prefix}{new_count}"

        # Update counter
        transaction.update(counter_ref, {
            "count": new_count,
            "prefix": prefix,
            "label": label,
        })

        return generated_user_id

    transaction = db.transaction()
    return transaction_op(transaction, counter_ref)


if __name__ == "__main__":
    print(generate_user_id())
