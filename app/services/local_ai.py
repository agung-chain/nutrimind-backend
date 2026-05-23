def calculate_bmi(weight, height):
    return weight / ((height / 100) ** 2)


def local_ai_analysis(data):
    bmi = calculate_bmi(data["weight"], data["height"])

    risk = "low"

    if data["stress_level"] >= 8 and data["sleep_hours"] < 6:
        risk = "high"

    elif bmi > 25:
        risk = "medium"

    elif data["mood"] <= 4:
        risk = "medium"

    return {
        "bmi": round(bmi, 2),
        "risk": risk
    }