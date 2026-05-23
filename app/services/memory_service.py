from app.database import db
from datetime import datetime

def save_memory(student_input, ai_output, source):
    db.ai_memory.insert_one({
        "input": student_input,
        "ai_advice": ai_output,
        "source": source
    })