from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import db
from app.routes.student_routes import router as student_router
from app.services.mbg_service import generate_mbg_menu
from app.services.warning_service import detect_warning
from app.services.student_ai_engine import get_student_ai_insight

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(student_router)

@app.get("/")
def root():
    return {
        "message": "NutriMind AI Backend Running"
    }

@app.get("/school-intelligence")
def school_intelligence():

    students = list(db.daily_checkins.find({}))

    total_students = len(students)

    high_stress = len([s for s in students if s.get("stress_level", 0) >= 7])

    low_sleep = len([s for s in students if s.get("sleep_hours", 0) < 6])

    low_mood = len([s for s in students if s.get("mood", 0) < 5])

    avg_bmi = 0
    bmi_count = 0

    for s in students:
        bmi = s.get("bmi", 0)

        if isinstance(bmi, dict):
            bmi = bmi.get("value", 0)

        if bmi:
            avg_bmi += bmi
            bmi_count += 1

    avg_bmi = avg_bmi / bmi_count if bmi_count > 0 else 0

    return {
        "total_students": total_students,
        "high_stress_cases": high_stress,
        "low_sleep_cases": low_sleep,
        "low_mood_cases": low_mood,
        "average_bmi": round(avg_bmi, 2),
        "risk_level": "HIGH" if high_stress > 5 else "NORMAL"
    }


@app.get("/health-alerts")
def health_alerts():

    # =====================================
    # AMBIL SEMUA DATA
    # =====================================

    all_data = list(

        db.daily_checkins.find().sort(
            "_id",
            -1
        )

    )

    # =====================================
    # FILTER STUDENT UNIK
    # =====================================

    latest_students = {}

    for student in all_data:

        uid = student.get(
            "student_uid"
        )

        # hanya ambil data terbaru

        if uid not in latest_students:

            latest_students[uid] = student

    students = list(
        latest_students.values()
    )

    # =====================================
    # ALERTS
    # =====================================

    alerts = {

        "high_risk": [],
        "warning": [],
        "normal": []

    }

    # =====================================
    # LOOP
    # =====================================

    for s in students:

        bmi = s.get("bmi", {})

        if isinstance(bmi, dict):

            bmi = bmi.get(
                "value",
                0
            )

        stress = s.get(
            "stress_level",
            0
        )

        sleep = s.get(
            "sleep_hours",
            0
        )

        mood = s.get(
            "mood",
            0
        )

        # 🔴 HIGH RISK

        if (
            stress >= 8
            or sleep < 5
            or mood <= 3
        ):

            alerts["high_risk"].append({

                "student_uid":
                    s.get(
                        "student_uid"
                    ),

                "name":
                    s.get(
                        "name"
                    ),

                "stress":
                    stress,

                "sleep":
                    sleep,

                "mood":
                    mood,

                "bmi":
                    bmi,

                "wellness":
                    s.get(
                        "wellness_score",
                        0
                    )

            })

        # 🟡 WARNING

        elif (
            stress >= 6
            or sleep < 6
            or mood <= 5
        ):

            alerts["warning"].append({

                "student_uid":
                    s.get(
                        "student_uid"
                    ),

                "name":
                    s.get(
                        "name"
                    ),

                "stress":
                    stress,

                "sleep":
                    sleep,

                "mood":
                    mood,

                "bmi":
                    bmi,

                "wellness":
                    s.get(
                        "wellness_score",
                        0
                    )

            })

        # 🟢 NORMAL

        else:

            alerts["normal"].append({

                "student_uid":
                    s.get(
                        "student_uid"
                    ),

                "name":
                    s.get(
                        "name"
                    ),

                "stress":
                    stress,

                "sleep":
                    sleep,

                "mood":
                    mood,

                "bmi":
                    bmi,

                "wellness":
                    s.get(
                        "wellness_score",
                        0
                    )

            })

    # =====================================
    # RETURN
    # =====================================

    return {

        "total_students":
            len(students),

        "high_risk_count":
            len(
                alerts["high_risk"]
            ),

        "warning_count":
            len(
                alerts["warning"]
            ),

        "normal_count":
            len(
                alerts["normal"]
            ),

        "alerts":
            alerts

    }

@app.post("/mbg-recommendation")
def mbg_recommendation(data: dict):
    menu = generate_mbg_menu(data)

    return {
        "message": "MBG recommendation generated",
        "menu": menu
    }

@app.get("/mbg-dashboard")
def mbg_dashboard():
    total = db.ai_memory.count_documents({})

    stress_cases = db.ai_memory.count_documents({
        "input.stress_level": {"$gte": 7}
    })

    sleep_cases = db.ai_memory.count_documents({
        "input.sleep_hours": {"$lt": 6}
    })

    return {
        "total_students": total,
        "stress_cases": stress_cases,
        "sleep_issue": sleep_cases
    }

@app.get("/leaderboard")
def leaderboard():

    students = list(
        db.daily_checkins.find({})
    )

    ranking = []

    for s in students:

        reward = s.get("reward_system", {})

        ranking.append({
            "name": s.get("name"),
            "points": reward.get("health_points", 0),
            "badge": reward.get("badge", ""),
            "level": reward.get("level", "")
        })

    ranking = sorted(
        ranking,
        key=lambda x: x["points"],
        reverse=True
    )

    return ranking[:10]

@app.get("/student-summary")
def student_summary():

    total = db.daily_checkins.count_documents({})

    avg_score = 0

    students = list(
        db.daily_checkins.find()
    )

    if len(students) > 0:

        total_score = 0

        for s in students:

            total_score += s.get(
                "wellness_score",
                0
            )

        avg_score = total_score / len(students)

    return {

        "total_checkins": total,

        "average_wellness":
            round(avg_score, 2)

    }

@app.get("/parent-monitor/{student_uid}")
def parent_monitor(
    student_uid: str
):

    latest = db.daily_checkins.find_one(

        {
            "student_uid":
                student_uid
        },

        sort=[("_id", -1)]

    )

    if not latest:

        return {

            "message":
                "No student data"

        }

    latest["_id"] = str(
        latest["_id"]
    )

    return latest
@app.get("/sppg-intelligence")
def sppg_intelligence():

    students = list(
        db.daily_checkins.find()
    )

    total_students = len(students)

    stress_high = 0

    sleep_low = 0

    bmi_high = 0

    for s in students:

        if s.get("stress_level", 0) >= 7:
            stress_high += 1

        if s.get("sleep_hours", 0) < 6:
            sleep_low += 1

        bmi_data = s.get("bmi", {})

        bmi_value = bmi_data.get("bmi", 0)

        if bmi_value >= 25:
            bmi_high += 1

    recommendations = []

    if stress_high > 0:

        recommendations.append(
            "Tambahkan makanan penenang saraf seperti pisang, susu, oatmeal."
        )

    if sleep_low > 0:

        recommendations.append(
            "Tambahkan menu energi stabil dan magnesium."
        )

    if bmi_high > 0:

        recommendations.append(
            "Kurangi makanan tinggi gula dan gorengan."
        )

    if len(recommendations) == 0:

        recommendations.append(
            "Kondisi sekolah stabil."
        )

    return {

        "total_students": total_students,

        "high_stress": stress_high,

        "sleep_problem": sleep_low,

        "high_bmi": bmi_high,

        "recommendations": recommendations
    }

@app.get("/school-warnings")
def school_warnings():

    students = list(
        db.daily_checkins.find()
    )

    total_warnings = 0

    burnout_cases = 0

    obesity_cases = 0

    for s in students:

        warnings = s.get(
            "warnings",
            []
        )

        total_warnings += len(warnings)

        for w in warnings:

            if "burnout" in w.lower():
                burnout_cases += 1

            if "obesitas" in w.lower():
                obesity_cases += 1

    return {

        "total_warnings":
            total_warnings,

        "burnout_cases":
            burnout_cases,

        "obesity_cases":
            obesity_cases
    }

@app.get("/school-predictions")
def school_predictions():

    students = list(
        db.daily_checkins.find()
    )

    burnout_risk = 0

    obesity_risk = 0

    mental_risk = 0

    for s in students:

        predictions = s.get(
            "predictions",
            []
        )

        for p in predictions:

            if "burnout" in p.lower():
                burnout_risk += 1

            if "obesitas" in p.lower():
                obesity_risk += 1

            if "mental" in p.lower():
                mental_risk += 1

    return {

        "burnout_risk":
            burnout_risk,

        "obesity_risk":
            obesity_risk,

        "mental_health_risk":
            mental_risk
    }

@app.get("/student-ai/{student_uid}")
def student_ai(student_uid: str):

    result = get_student_ai_insight(student_uid)

    return {
        "message": "AI insight generated",
        "data": result
    }

@app.get("/user/{email}")
def get_user(email: str):
    user = db.users.find_one({"email": email})

    if not user:
        return {"error": "user not found"}

    user["_id"] = str(user["_id"])
    return user


@app.get("/checkin/{student_uid}")
def get_latest_checkin(student_uid: str):

    data = db.daily_checkins.find_one(
        {"student_uid": student_uid},
        sort=[("created_at", -1)]
    )

    if not data:
        return {}

    data["_id"] = str(data["_id"])

    return data

@app.post("/save-profile")
def save_profile(data: dict):

    # 🔥 AUTO GENERATE UID
    student_uid = f"{data['school_code']}-{data['nis']}"

    profile = {
        "email": data["email"],
        "student_uid": student_uid,
        "school_code": data["school_code"],
        "nis": data["nis"],
        "name": data["name"],
        "age": data["age"],
        "height": data["height"],
        "weight": data["weight"]
    }

    # upsert = update kalau ada, insert kalau belum ada
    db.users.update_one(
        {"email": data["email"]},
        {"$set": profile},
        upsert=True
    )

    return {
        "success": True,
        "student_uid": student_uid
    }