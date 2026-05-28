from fastapi import APIRouter
from app.models.student_model import StudentCheckin
from datetime import datetime, timezone

# DATABASE
from app.database import db

# UTILITIES
from app.utils.bmi import calculate_bmi
from app.utils.wellness_score import calculate_wellness_score

# SERVICES
from app.services.gemini_service import generate_health_advice
from app.services.reward_service import calculate_reward
from app.services.warning_service import detect_warning
from app.services.prediction_service import predict_health
from app.services.memory_service import save_memory
from app.services.pattern_service import (
    extract_pattern,
    save_pattern,
    extract_pattern_ai
)

router = APIRouter()


@router.post("/checkin")
def student_checkin(data: StudentCheckin):

    try:

        # =========================
        # BASIC DATA
        # =========================

        student_uid = f"{data.school_code}-{data.nis}"

        # =========================
        # LIMIT 1 CHECKIN / HARI
        # =========================

        today = datetime.now(timezone.utc).date()

        existing = db.daily_checkins.find_one({
            "student_uid": student_uid,
            "checkin_date": str(today)
        })

        if existing:

            return {
                "success": False,
                "message": "Kamu sudah check-in hari ini 😊"
            }

        student_data = data.dict()

        student_data["student_uid"] = student_uid

        print("\n===== CHECKIN DATA =====")
        print(student_data)
        print("========================\n")

        # =========================
        # BMI
        # =========================

        bmi_result = calculate_bmi(
            data.weight,
            data.height
        )

        student_data["bmi"] = bmi_result

        # =========================
        # WELLNESS SCORE
        # =========================

        wellness_score = calculate_wellness_score(data)

        student_data["wellness_score"] = wellness_score

        # =========================
        # WARNINGS
        # =========================

        warnings = detect_warning(student_data)

        student_data["warnings"] = warnings

        # =========================
        # HEALTH PREDICTION
        # =========================

        predictions = predict_health(student_data)

        student_data["predictions"] = predictions

        # =========================
        # REWARD SYSTEM
        # =========================

        reward_data = calculate_reward(student_data)

        student_data["reward_system"] = reward_data

        # =========================
        # AI ANALYSIS
        # =========================

        ai_advice = generate_health_advice(student_data)

        student_data["ai_advice"] = ai_advice

        # =========================
        # PATTERN ANALYSIS
        # =========================

        pattern = extract_pattern_ai(student_data)

        save_pattern(pattern)

        # =========================
        # MEMORY SAVE
        # =========================

        save_memory(
            student_input=student_data,
            ai_output=ai_advice,
            source="gemini/local"
        )

        # =========================
        # SAVE TO DATABASE
        # =========================
        student_data["created_at"] = datetime.now(timezone.utc)
        student_data["checkin_date"] = str(today)
        
        result = db.daily_checkins.insert_one(student_data)

        student_data["_id"] = str(result.inserted_id)

        # =========================
        # SUCCESS RESPONSE
        # =========================

        return {
            "success": True,
            "message": "Check-in successful",
            "data": student_data
        }

    except Exception as e:

        print("\n===== ERROR CHECKIN =====")
        print(str(e))
        print("=========================\n")

        return {
            "success": False,
            "message": str(e)
        }