from app.services.memory_service import save_memory
from app.services.pattern_service import extract_pattern, save_pattern, extract_pattern_ai
from fastapi import APIRouter
from app.models.student_model import StudentCheckin
from app.utils.bmi import calculate_bmi
from app.utils.wellness_score import calculate_wellness_score
from app.database import db
from app.services.gemini_service import generate_health_advice
from app.services.reward_service import calculate_reward
from app.services.warning_service import detect_warning
from app.services.prediction_service import predict_health
from fastapi import Request
router = APIRouter()
@router.post("/checkin")
def student_checkin(data: StudentCheckin):

    student_uid = f"{data.school_code}-{data.nis}"
    bmi_result = calculate_bmi(
        data.weight,
        data.height
    )

    wellness_score = calculate_wellness_score(data)

    student_data = data.dict()
    student_data["student_uid"] = student_uid
    student_data["bmi"] = bmi_result
    student_data["wellness_score"] = wellness_score
    warnings = detect_warning(student_data)
    student_data["warnings"] = warnings
    predictions = predict_health(student_data)
    student_data["predictions"] = predictions
    reward_data = calculate_reward(student_data)
    student_data["reward_system"] = reward_data
    # AI Gemini analysis
    ai_advice = generate_health_advice(student_data)
    pattern = extract_pattern_ai(student_data)
    save_pattern(pattern)
    save_memory(
        student_input=student_data,
        ai_output=ai_advice,
        source="gemini/local"
    )
    student_data["ai_advice"] = ai_advice

    result = db.daily_checkins.insert_one(student_data)

    student_data["_id"] = str(result.inserted_id)

    return {
        "message": "Check-in successful",
        "data": student_data
    }
