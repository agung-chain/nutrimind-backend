from pymongo import MongoClient
from dotenv import load_dotenv
import os
import traceback

# LOAD ENV
load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")

print("MONGO URI:")
print(MONGO_URI)

try:

    # CONNECT
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000
    )

    # TEST CONNECTION
    client.admin.command("ping")

    print("✅ MongoDB Connected!")

    # DATABASE
    db = client["nutrimind_ai"]

    # TEST DATA
    profile = {
        "email": "test@gmail.com",
        "name": "Agung",
        "student_uid": "STD001",
        "age": 15
    }

    print("🚀 Saving profile...")

    result = db.users.update_one(
        {"email": profile["email"]},
        {"$set": profile},
        upsert=True
    )

    print("✅ SUCCESS SAVE")

    print("Matched:", result.matched_count)
    print("Modified:", result.modified_count)
    print("Upserted ID:", result.upserted_id)

    # READ BACK
    user = db.users.find_one({
        "email": "test@gmail.com"
    })

    print("📦 DATA IN DB:")
    print(user)

except Exception as e:

    print("❌ ERROR:")
    print(str(e))

    print("\nFULL TRACEBACK:\n")
    traceback.print_exc()