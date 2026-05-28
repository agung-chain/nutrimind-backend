from pymongo import MongoClient
from dotenv import load_dotenv
import os

# LOAD ENV
load_dotenv()

MONGO_URL = os.getenv("MONGODB_URI")

print("MONGO_URL:", MONGO_URL)

try:

    client = MongoClient(
        MONGO_URL,
        tls=True,
        tlsAllowInvalidCertificates=True
    )

    # TEST CONNECTION
    client.admin.command("ping")

    print("✅ MongoDB Connected!")

    db = client["nutrimind_ai"]

    collections = db.list_collection_names()

    print("Collections:")
    print(collections)

except Exception as e:

    print("❌ Connection Failed")
    print(e)