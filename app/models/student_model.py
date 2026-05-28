from pydantic import BaseModel

class StudentCheckin(BaseModel):

    # BASIC
    name: str
    age: int

    # BODY
    height: float
    weight: float

    # WELLNESS
    mood: int
    sleep_hours: float
    exercise_minutes: int
    stress_level: int

    # NUTRITION
    water_intake: float
    breakfast: bool

    # IDENTITY
    school_code: str
    nis: str