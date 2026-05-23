from app.database import db

import google.generativeai as genai

# 🔥 GEMINI CONFIG
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(

    api_key=os.getenv(
        "GEMINI_API_KEY"
    )

)
'''
genai.configure(

    api_key="AIzaSyBJNUduVhjGx9FIYXwL8o7ZaDRB3e99_UE"

)
'''
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


# =========================================
# LOCAL AI ENGINE
# =========================================

def local_ai_analysis(
    avg_stress,
    avg_sleep,
    avg_mood,
    stress_trend,
    sleep_trend,
    mood_trend,
    health_score
):

    analysis = ""

    # STRESS

    if avg_stress >= 7:

        analysis += (
            "😣 Akhir-akhir ini "
            "pikiran kamu cukup berat.\n\n"
        )

    elif avg_stress >= 4:

        analysis += (
            "🙂 Kadang ada hal yang "
            "cukup bikin kepikiran.\n\n"
        )

    else:

        analysis += (
            "😌 Pikiran kamu cukup "
            "tenang minggu ini.\n\n"
        )

    # TIDUR

    if avg_sleep < 6:

        analysis += (
            "😴 Jam tidur kamu "
            "masih kurang.\n\n"
        )

    else:

        analysis += (
            "🌙 Pola tidur kamu "
            "cukup baik.\n\n"
        )

    # MOOD

    if avg_mood >= 8:

        analysis += (
            "😊 Mood kamu cukup "
            "positif akhir-akhir ini.\n\n"
        )

    else:

        analysis += (
            "💛 Tetap semangat "
            "menjalani harimu.\n\n"
        )

    # HEALTH SCORE

    if health_score >= 80:

        analysis += (
            "🏆 Kondisi kesehatan kamu "
            "sangat baik!"
        )

    elif health_score >= 60:

        analysis += (
            "🌱 Kondisi kamu cukup baik "
            "dan terus berkembang."
        )

    else:

        analysis += (
            "💪 Yuk pelan-pelan "
            "perbaiki pola sehat kamu."
        )

    return analysis


# =========================================
# GEMINI AI ENGINE
# =========================================

def gemini_ai_analysis(prompt):

    response = model.generate_content(
        prompt
    )

    return response.text


# =========================================
# MAIN AI ENGINE
# =========================================

def get_student_ai_insight(
    student_uid: str
):

    data = list(

        db.daily_checkins.find({

            "student_uid":
                student_uid

        })

    )

    if len(data) == 0:

        return {

            "status": "no_data"

        }

    data = data[-7:]

    stress_list = []
    sleep_list = []
    mood_list = []

    for d in data:

        stress_list.append(
            d.get(
                "stress_level",
                0
            )
        )

        sleep_list.append(
            d.get(
                "sleep_hours",
                0
            )
        )

        mood_list.append(
            d.get(
                "mood",
                0
            )
        )

    # =========================================
    # TREND
    # =========================================

    stress_trend = (
        stress_list[-1]
        - stress_list[0]
    ) if len(stress_list) > 1 else 0

    sleep_trend = (
        sleep_list[-1]
        - sleep_list[0]
    ) if len(sleep_list) > 1 else 0

    mood_trend = (
        mood_list[-1]
        - mood_list[0]
    ) if len(mood_list) > 1 else 0

    avg_stress = (
        sum(stress_list)
        / len(stress_list)
    )

    avg_sleep = (
        sum(sleep_list)
        / len(sleep_list)
    )

    avg_mood = (
        sum(mood_list)
        / len(mood_list)
    )

    # =========================================
    # HEALTH SCORE
    # =========================================

    health_score = (

        avg_mood * 10

        + avg_sleep * 5

        - avg_stress * 5

    )

    if health_score > 100:
        health_score = 100

    if health_score < 0:
        health_score = 0

    # =========================================
    # GEMINI PROMPT
    # =========================================

    # =========================================
# BUILD HISTORY
# =========================================

    history_text = ""

    for index, d in enumerate(data):

        history_text += f"""

    Hari {index + 1}

    - Mood:
    {d.get("mood", 0)}

    - Tidur:
    {d.get("sleep_hours", 0)} jam

    - Pikiran:
    {d.get("stress_level", 0)}

    - Olahraga:
    {d.get("exercise_minutes", 0)} menit

    """

    # =========================================
    # GEMINI PROMPT
    # =========================================

    prompt = f"""

    Kamu adalah AI wellness companion
    untuk siswa SMP/SMA.

    Tugas kamu:
    - membaca pola kesehatan siswa
    - memahami perubahan emosi siswa
    - memberi motivasi hangat
    - gunakan bahasa santai modern
    - jangan terlalu formal
    - jangan seperti dokter
    - gunakan emoji seperlunya

    =================================

    DATA 7 HARI SISWA:

    {history_text}

    =================================

    RATA-RATA:

    - Stress:
    {avg_stress}

    - Tidur:
    {avg_sleep}

    - Mood:
    {avg_mood}

    =================================

    TREND:

    - Stress trend:
    {stress_trend}

    - Sleep trend:
    {sleep_trend}

    - Mood trend:
    {mood_trend}

    =================================

    HEALTH SCORE:

    {health_score}

    =================================

    Berikan:

    1. Insight kondisi siswa
    2. Perubahan yang terlihat
    3. Motivasi pendek
    4. Saran sederhana sehari-hari

    Gunakan gaya bahasa:
    - hangat
    - suportif
    - modern
    - seperti teman digital

    """

    # =========================================
    # TRY GEMINI
    # =========================================

    try:

        analysis = gemini_ai_analysis(
            prompt
        )

        ai_source = "gemini"

    # =========================================
    # FALLBACK LOCAL AI
    # =========================================

    except Exception as e:

        print(
            "Gemini Error:",
            e
        )

        analysis = local_ai_analysis(

            avg_stress,
            avg_sleep,
            avg_mood,
            stress_trend,
            sleep_trend,
            mood_trend,
            health_score

        )

        ai_source = "local_ai"

    # =========================================
    # RETURN
    # =========================================

    return {

        "status": "ok",

        "student": student_uid,

        "health_score": round(
            health_score,
            2
        ),

        "ai_source": ai_source,

        "analysis": analysis

    }