from app.database import db

def extract_pattern(data):
    stress = data.get("stress_level", 0)
    sleep = data.get("sleep_hours", 0)

    if stress >= 7 and sleep < 6:
        return "stress_high_sleep_low"
    elif stress >= 7:
        return "stress_high"
    elif sleep < 6:
        return "sleep_low"
    else:
        return "normal"


def save_pattern(pattern):
    db.ai_patterns.update_one(
        {"pattern": pattern},
        {"$inc": {"count": 1}},
        upsert=True
    )

def extract_pattern_ai(data):

    stress = data.get("stress_level", 0)
    sleep = data.get("sleep_hours", 0)
    mood = data.get("mood", 0)

    score = 0

    # 🔴 stress weight
    if stress >= 8:
        score += 3
    elif stress >= 6:
        score += 2

    # 😴 sleep weight
    if sleep < 5:
        score += 3
    elif sleep < 6:
        score += 2

    # 😐 mood weight
    if mood <= 3:
        score += 3
    elif mood <= 5:
        score += 2

    # 📊 hasil AI pattern level
    if score >= 7:
        return "critical_risk"
    elif score >= 4:
        return "warning_risk"
    else:
        return extract_pattern(data)  # fallback ke sistem lama