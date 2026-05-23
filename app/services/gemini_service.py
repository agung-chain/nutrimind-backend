from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

# =========================
# GEMINI CLIENT
# =========================

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# =========================
# LOCAL AI FALLBACK
# =========================
def local_ai_analysis(student_data):

    advice = []

    bmi = student_data["bmi"]["bmi"]
    bmi_category = student_data["bmi"]["category"]

    mood = student_data["mood"]
    sleep = student_data["sleep_hours"]
    exercise = student_data["exercise_minutes"]
    stress = student_data["stress_level"]

    # =========================
    # ANALISA BMI
    # =========================

    if bmi < 18.5:

        advice.append(
            "⚠️ Kondisi berat badan siswa tergolong di bawah normal. "
            "Siswa berpotensi mengalami kekurangan asupan energi dan protein."
        )

        advice.append(
            "🍗 Rekomendasi gizi: tambahkan protein seperti telur, ayam, ikan, tempe, tahu, dan susu."
        )

    elif bmi > 25:

        advice.append(
            "⚠️ Berat badan siswa tergolong berlebih. "
            "Perlu pengaturan pola makan dan aktivitas fisik."
        )

        advice.append(
            "🥗 Kurangi makanan tinggi gula dan gorengan. "
            "Perbanyak sayur, buah, dan aktivitas olahraga."
        )

    else:

        advice.append(
            "✅ BMI siswa berada pada kategori normal."
        )

    # =========================
    # ANALISA TIDUR
    # =========================

    if sleep < 6:

        advice.append(
            "😴 Jam tidur siswa sangat kurang. "
            "Kurang tidur dapat menurunkan fokus belajar dan kesehatan mental."
        )

    elif sleep < 8:

        advice.append(
            "🛌 Jam tidur siswa masih kurang optimal. "
            "Disarankan tidur lebih awal untuk mendukung pertumbuhan."
        )

    else:

        advice.append(
            "🌙 Pola tidur siswa cukup baik."
        )

    # =========================
    # ANALISA STRESS
    # =========================

    if stress >= 8:

        advice.append(
            "🚨 Tingkat stres siswa sangat tinggi. "
            "Perlu perhatian dari orang tua atau guru BK."
        )

    elif stress >= 5:

        advice.append(
            "⚠️ Siswa mulai menunjukkan tingkat stres sedang."
        )

    else:

        advice.append(
            "😊 Tingkat stres siswa relatif stabil."
        )

    # =========================
    # ANALISA MOOD
    # =========================

    if mood <= 4:

        advice.append(
            "💭 Mood siswa rendah. "
            "Perlu dukungan sosial, aktivitas menyenangkan, dan komunikasi positif."
        )

    elif mood <= 7:

        advice.append(
            "🙂 Kondisi emosional siswa cukup baik."
        )

    else:

        advice.append(
            "😄 Mood siswa sangat baik dan positif."
        )

    # =========================
    # ANALISA OLAHRAGA
    # =========================

    if exercise < 20:

        advice.append(
            "🏃 Aktivitas fisik siswa masih sangat kurang."
        )

    elif exercise < 45:

        advice.append(
            "🚶 Aktivitas fisik siswa cukup, tetapi masih bisa ditingkatkan."
        )

    else:

        advice.append(
            "💪 Aktivitas fisik siswa sangat baik."
        )

    # =========================
    # REKOMENDASI MBG
    # =========================

    advice.append(
        "🍱 Rekomendasi Menu MBG Hari Ini:"
    )

    if bmi < 18.5:

        advice.append(
            "- Nasi\n- Telur\n- Tempe\n- Sayur bayam\n- Susu\n- Pisang"
        )

    elif bmi > 25:

        advice.append(
            "- Nasi secukupnya\n- Ikan panggang\n- Sayur hijau\n- Buah segar\n- Air putih"
        )

    else:

        advice.append(
            "- Nasi\n- Ayam\n- Sayur\n- Buah\n- Susu"
        )

    # =========================
    # KESIMPULAN
    # =========================

    advice.append(
        "\n📊 Sistem AI menyarankan pemantauan rutin setiap minggu "
        "untuk melihat perkembangan kesehatan fisik dan mental siswa."
    )

    return "\n\n".join(advice)

def local_ai_analysis2(student_data):

    advice = []

    bmi = student_data["bmi"]["bmi"]

    mood = student_data["mood"]
    sleep = student_data["sleep_hours"]
    exercise = student_data["exercise_minutes"]
    stress = student_data["stress_level"]
    
    # BMI
    if bmi < 18.5:

        advice.append(
            "⚠️ Berat badan siswa di bawah normal."
        )

        advice.append(
            "🍗 Tambahkan protein dan susu."
        )

    elif bmi > 25:

        advice.append(
            "⚠️ Berat badan siswa berlebih."
        )

        advice.append(
            "🥗 Kurangi gula dan gorengan."
        )

    else:

        advice.append(
            "✅ BMI siswa normal."
        )

    # Sleep
    if sleep < 7:

        advice.append(
            "😴 Jam tidur siswa kurang."
        )

    # Stress
    if stress >= 7:

        advice.append(
            "🚨 Tingkat stres siswa tinggi."
        )

    # Mood
    if mood <= 4:

        advice.append(
            "💭 Mood siswa rendah."
        )

    # Exercise
    if exercise < 30:

        advice.append(
            "🏃 Aktivitas fisik siswa kurang."
        )

    # MBG
    advice.append(
        "🍱 Rekomendasi MBG: nasi, telur, tempe, sayur, susu."
    )

    advice.append(
        "\n🤖 Analisa menggunakan Local NutriMind AI."
    )

    return "\n\n".join(advice)

# =========================
# GEMINI + FALLBACK
# =========================

def generate_health_advice(student_data):

    try:

        prompt = f"""
        Anda adalah AI kesehatan sekolah Indonesia.

        Analisa data siswa berikut:

        Nama: {student_data["name"]}
        Umur: {student_data["age"]}
        BMI: {student_data["bmi"]["bmi"]}
        Kategori BMI: {student_data["bmi"]["category"]}
        Mood: {student_data["mood"]}
        Jam tidur: {student_data["sleep_hours"]}
        Olahraga: {student_data["exercise_minutes"]}
        Stress: {student_data["stress_level"]}

        Berikan:
        1. Analisa kesehatan fisik
        2. Analisa mental
        3. Saran untuk sekolah
        4. Saran untuk orang tua
        5. Rekomendasi menu MBG
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return (
            response.text +
            "\n\n🤖 Analisa menggunakan Gemini AI."
        )

    except Exception as e:

        print("Gemini Error:", e)

        return local_ai_analysis(student_data)