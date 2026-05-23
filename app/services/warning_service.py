def detect_warning(data):

    warnings = []

    stress = data.get("stress_level", 0)

    sleep = data.get("sleep_hours", 0)

    mood = data.get("mood", 0)

    bmi_data = data.get("bmi", {})

    bmi = bmi_data.get("bmi", 0)

    if stress >= 8:

        warnings.append(
            "Stress sangat tinggi"
        )

    if sleep < 5:

        warnings.append(
            "Kurang tidur serius"
        )

    if mood <= 3:

        warnings.append(
            "Mood sangat rendah"
        )

    if bmi >= 30:

        warnings.append(
            "Risiko obesitas"
        )

    if stress >= 8 and sleep < 5:

        warnings.append(
            "Risiko burnout siswa"
        )

    return warnings