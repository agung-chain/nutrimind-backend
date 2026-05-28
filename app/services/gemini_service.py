from google import genai
from dotenv import load_dotenv
import os
import random

load_dotenv()

# =========================
# GEMINI CLIENT
# =========================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# =========================
# RANDOM RESPONSE HELPER
# =========================

def pick(options):
    return random.choice(options)

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

    water = student_data.get("water_intake", 0)
    breakfast = student_data.get("breakfast", False)

    # =========================
    # OPENING
    # =========================

    advice.append(
        pick([
            "📊 Berikut analisa kesehatan siswa hari ini.",
            "🧠 Sistem wellness mendeteksi kondisi siswa sebagai berikut.",
            "📈 AI menemukan beberapa pola penting dari check-in siswa."
        ])
    )

    # =========================
    # BMI ANALYSIS
    # =========================

    if bmi < 18.5:

        advice.append(
            pick([
                "⚠️ BMI berada di bawah normal sehingga siswa berpotensi kekurangan energi.",
                "🍚 Berat badan siswa masih tergolong kurang dan perlu peningkatan nutrisi.",
                "🥛 Sistem mendeteksi kemungkinan kurang asupan protein dan kalori."
            ])
        )

        advice.append(
            pick([
                "🍗 Tambahkan telur, susu, ikan, tempe, dan buah.",
                "🥚 Disarankan konsumsi protein lebih rutin setiap hari.",
                "🍌 Menu tinggi energi sehat sangat dianjurkan."
            ])
        )

    elif bmi > 25:

        advice.append(
            pick([
                "⚠️ BMI berada di atas normal.",
                "🍟 Berat badan siswa tergolong berlebih.",
                "🥤 AI mendeteksi risiko pola makan kurang sehat."
            ])
        )

        advice.append(
            pick([
                "🥗 Kurangi minuman manis dan gorengan.",
                "🏃 Tingkatkan aktivitas fisik harian.",
                "🍎 Perbanyak sayur, buah, dan air putih."
            ])
        )

    else:

        advice.append(
            pick([
                "✅ BMI siswa berada pada kategori ideal.",
                "💪 Berat badan siswa cukup seimbang.",
                "🌟 Kondisi fisik siswa relatif stabil."
            ])
        )

    # =========================
    # MOOD ANALYSIS
    # =========================

    if mood <= 3:

        advice.append(
            pick([
                "😟 Mood siswa sangat rendah hari ini.",
                "💭 Emosi siswa tampak kurang stabil.",
                "🫤 Siswa terlihat mengalami penurunan semangat."
            ])
        )

    elif mood <= 7:

        advice.append(
            pick([
                "🙂 Mood siswa cukup baik.",
                "😊 Kondisi emosional relatif stabil.",
                "🌤️ Siswa berada dalam kondisi emosi sedang."
            ])
        )

    else:

        advice.append(
            pick([
                "😄 Mood siswa sangat positif.",
                "🌈 Kondisi emosional siswa sangat baik.",
                "✨ Semangat dan suasana hati siswa terlihat bagus."
            ])
        )

    # =========================
    # SLEEP ANALYSIS
    # =========================

    if sleep < 6:

        advice.append(
            pick([
                "😴 Jam tidur sangat kurang.",
                "🌙 Kurang tidur dapat memengaruhi fokus belajar.",
                "🛌 AI mendeteksi pola tidur tidak sehat."
            ])
        )

    elif sleep < 8:

        advice.append(
            pick([
                "🛏️ Tidur cukup tetapi belum optimal.",
                "🌜 Waktu tidur siswa masih bisa ditingkatkan.",
                "💤 Kualitas istirahat cukup baik."
            ])
        )

    else:

        advice.append(
            pick([
                "🌙 Pola tidur siswa sangat baik.",
                "😴 Waktu istirahat cukup untuk mendukung pertumbuhan.",
                "💤 Sistem mendeteksi kualitas tidur yang sehat."
            ])
        )

    # =========================
    # STRESS ANALYSIS
    # =========================

    if stress >= 8:

        advice.append(
            pick([
                "🚨 Tingkat stres sangat tinggi.",
                "⚠️ Siswa membutuhkan perhatian emosional tambahan.",
                "🧠 Risiko kelelahan mental cukup tinggi."
            ])
        )

    elif stress >= 5:

        advice.append(
            pick([
                "⚠️ Tingkat stres sedang.",
                "📚 Siswa mulai mengalami tekanan aktivitas.",
                "🧠 Beban mental siswa perlu dipantau."
            ])
        )

    else:

        advice.append(
            pick([
                "😊 Tingkat stres relatif stabil.",
                "🌿 Kondisi mental siswa cukup baik.",
                "🧘 Siswa terlihat cukup tenang."
            ])
        )

    # =========================
    # EXERCISE ANALYSIS
    # =========================

    if exercise < 20:

        advice.append(
            pick([
                "🏃 Aktivitas fisik masih sangat kurang.",
                "🚶 Tubuh membutuhkan lebih banyak gerakan aktif.",
                "⚡ Siswa disarankan lebih rutin berolahraga."
            ])
        )

    elif exercise < 45:

        advice.append(
            pick([
                "💪 Aktivitas fisik cukup baik.",
                "🏃 Siswa cukup aktif bergerak.",
                "🚴 Olahraga siswa sudah lumayan bagus."
            ])
        )

    else:

        advice.append(
            pick([
                "🔥 Aktivitas fisik sangat baik.",
                "💯 Siswa sangat aktif hari ini.",
                "🏆 Kebiasaan olahraga siswa sangat positif."
            ])
        )

    # =========================
    # WATER ANALYSIS
    # =========================

    if water < 4:

        advice.append(
            pick([
                "💧 Konsumsi air masih sangat kurang.",
                "🚰 Tubuh membutuhkan lebih banyak cairan.",
                "🥤 Risiko dehidrasi ringan terdeteksi."
            ])
        )

    elif water < 7:

        advice.append(
            pick([
                "💦 Konsumsi air cukup baik.",
                "🚰 Hidrasi siswa lumayan stabil.",
                "🥛 Asupan cairan cukup tetapi bisa ditingkatkan."
            ])
        )

    else:

        advice.append(
            pick([
                "💧 Hidrasi siswa sangat baik.",
                "🌊 Konsumsi air harian sudah ideal.",
                "🚰 Tubuh siswa terhidrasi dengan baik."
            ])
        )

    # =========================
    # BREAKFAST ANALYSIS
    # =========================

    if breakfast:

        advice.append(
            pick([
                "🍞 Sarapan membantu menjaga fokus belajar.",
                "🥣 Kebiasaan sarapan siswa sangat baik.",
                "🍳 Energi pagi siswa tercukupi."
            ])
        )

    else:

        advice.append(
            pick([
                "⚠️ Siswa tidak sarapan hari ini.",
                "🍞 Melewatkan sarapan dapat menurunkan konsentrasi.",
                "🥐 Sistem menyarankan sarapan sehat sebelum sekolah."
            ])
        )

    # =========================
    # MBG RECOMMENDATION
    # =========================

    advice.append("\n🍱 Rekomendasi Menu MBG:")

    if bmi < 18.5:

        advice.append(
            pick([
                "- Nasi\n- Ayam\n- Telur\n- Tempe\n- Susu\n- Pisang",
                "- Nasi\n- Ikan\n- Sayur bayam\n- Susu\n- Buah",
                "- Nasi\n- Telur rebus\n- Tahu\n- Sayur hijau\n- Susu"
            ])
        )

    elif bmi > 25:

        advice.append(
            pick([
                "- Nasi secukupnya\n- Ikan panggang\n- Sayur hijau\n- Buah",
                "- Sup sayur\n- Ayam rebus\n- Air putih",
                "- Oatmeal\n- Telur\n- Salad buah"
            ])
        )

    else:

        advice.append(
            pick([
                "- Nasi\n- Ayam\n- Sayur\n- Buah\n- Susu",
                "- Nasi\n- Ikan\n- Tempe\n- Sayur hijau",
                "- Nasi\n- Telur\n- Sayur sop\n- Buah"
            ])
        )

    # =========================
    # FINAL SUMMARY
    # =========================

    advice.append(
        "\n📌 Sistem menyarankan pemantauan rutin mingguan untuk melihat perkembangan kesehatan siswa."
    )

    advice.append(
        "🤖 Analisa dibuat menggunakan Local Wellness AI."
    )

    return "\n\n".join(advice)

# =========================
# GEMINI + FALLBACK
# =========================

def generate_health_advice(student_data):

    try:

        prompt = f"""
Anda adalah AI wellness, nutrition, dan mental health assistant
untuk siswa sekolah Indonesia.

Tugas:
- analisa kesehatan siswa
- gunakan bahasa sederhana
- jangan terlalu medis
- hangat dan suportif
- maksimal 300 kata
- gunakan emoji seperlunya
- fokus pada:
  * fisik
  * mental
  * pola hidup
  * nutrisi
  * hidrasi
  * sarapan
  * aktivitas sekolah

DATA SISWA

Nama: {student_data["name"]}
Umur: {student_data["age"]}

BMI: {student_data["bmi"]["bmi"]}
Kategori BMI: {student_data["bmi"]["category"]}

Mood: {student_data["mood"]}
Tidur: {student_data["sleep_hours"]}
Olahraga: {student_data["exercise_minutes"]}
Stress: {student_data["stress_level"]}

Minum Air: {student_data.get("water_intake", 0)}
Sarapan: {student_data.get("breakfast", False)}

Berikan output dengan format:

📊 Kondisi Umum
🧠 Mental & Emosi
💪 Fisik & Aktivitas
💧 Hidrasi & Nutrisi
🏫 Saran Sekolah
👨‍👩‍👧 Saran Orang Tua
🍱 Rekomendasi Makanan Bergizi
📌 Kesimpulan
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