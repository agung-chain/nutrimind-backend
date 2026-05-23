from google import genai
from dotenv import load_dotenv
import os

# Load ENV
load_dotenv()

# Ambil API KEY
API_KEY = os.getenv("GEMINI_API_KEY")

print("API KEY:", API_KEY)

# Gemini Client
client = genai.Client(api_key=API_KEY)

# Generate AI Response
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Give health advice for students with poor sleep habits."
)

print("\n=== AI RESPONSE ===\n")
print(response.text)