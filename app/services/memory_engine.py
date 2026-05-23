from app.database import db
from datetime import datetime

from app.database import db

def save_pattern(pattern):
    if not pattern:
        return

    existing = db.ai_patterns.find_one({"pattern": pattern})

    if existing:
        db.ai_patterns.update_one(
            {"pattern": pattern},
            {"$inc": {"count": 1}}
        )
    else:
        db.ai_patterns.insert_one({
            "pattern": pattern,
            "count": 1,
            "risk_level": "medium"
        })
        
def save_ai_history(student_data, ai_result, source="local"):
    db.ai_history.insert_one({
        "student": student_data,
        "ai_result": ai_result,
        "source": source,
        "timestamp": datetime.utcnow()
    })

def detect_pattern(data):
    pattern = []

    if data["stress_level"] >= 7:
        pattern.append("stress_high")

    if data["sleep_hours"] < 6:
        pattern.append("sleep_low")

    if data["mood"] <= 5:
        pattern.append("mood_low")

    return "_".join(pattern)

