# app/services/mbg_service.py

def generate_mbg_menu(data):
    stress = data.get("stress_level", 0)
    sleep = data.get("sleep_hours", 0)
    mood = data.get("mood", 5)
    bmi = data.get("bmi", 0)

    menu = {
        "breakfast": [],
        "lunch": [],
        "dinner": [],
        "snack": [],
        "reason": []
    }

    # 🧠 RULE 1: STRESS TINGGI
    if stress >= 7:
        menu["breakfast"].append("Oatmeal + pisang + madu")
        menu["snack"].append("Coklat hitam + kacang almond")
        menu["reason"].append("Stress tinggi → makanan penenang saraf")

    # 😴 RULE 2: KURANG TIDUR
    if sleep < 6:
        menu["breakfast"].append("Telur + roti gandum")
        menu["lunch"].append("Nasi merah + ayam + sayur hijau")
        menu["reason"].append("Kurang tidur → butuh energi stabil")

    # ⚖️ RULE 3: BMI NORMAL/OVER
    if bmi > 23:
        menu["lunch"].append("Sayur rebus + ikan panggang")
        menu["dinner"].append("Sup sayur ringan")
        menu["reason"].append("BMI tinggi → diet rendah lemak")

    # 😊 RULE 4: MOOD RENDAH
    if mood < 5:
        menu["snack"].append("Buah berry + yoghurt")
        menu["reason"].append("Mood rendah → serotonin booster")

    # default fallback
    if not menu["breakfast"]:
        menu["breakfast"].append("Nasi + telur + sayur")

    return menu