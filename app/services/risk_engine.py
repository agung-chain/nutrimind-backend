def risk_alert(data):
    if data["stress_level"] >= 8 and data["sleep_hours"] < 6:
        return "HIGH_RISK"

    if data["mood"] <= 4:
        return "MEDIUM_RISK"

    if data["weight"] / ((data["height"]/100) ** 2) > 25:
        return "MEDIUM_RISK"

    return "LOW_RISK"