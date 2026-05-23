def predict_health(data):

    predictions = []

    stress = data.get(
        "stress_level",
        0
    )

    sleep = data.get(
        "sleep_hours",
        0
    )

    mood = data.get(
        "mood",
        0
    )

    bmi_data = data.get(
        "bmi",
        {}
    )

    bmi = bmi_data.get(
        "bmi",
        0
    )

    # 🔴 Burnout prediction

    if stress >= 7 and sleep < 6:

        predictions.append(
            "Potensi burnout dalam beberapa minggu."
        )

    # 🔴 Obesity prediction

    if bmi >= 27:

        predictions.append(
            "Risiko obesitas meningkat."
        )

    # 🔴 Mental health prediction

    if mood <= 4 and stress >= 7:

        predictions.append(
            "Risiko gangguan mental/emotional."
        )

    # 🟡 Sleep prediction

    if sleep < 6:

        predictions.append(
            "Performa akademik berpotensi menurun."
        )

    # 🟢 Healthy prediction

    if len(predictions) == 0:

        predictions.append(
            "Kondisi kesehatan cenderung stabil."
        )

    return predictions