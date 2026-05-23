from pydantic import BaseModel

class StudentCheckin(BaseModel):
    name: str
    age: int
    height: float
    weight: float
    mood: int
    sleep_hours: float
    exercise_minutes: int
    stress_level: int
    school_code: str
    nis: str