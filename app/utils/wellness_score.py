def calculate_wellness_score(data):
    score = 100

    # Sleep
    if data.sleep_hours < 6:
        score -= 20

    # Stress
    if data.stress_level > 7:
        score -= 20

    # Exercise
    if data.exercise_minutes < 20:
        score -= 15

    # Mood
    if data.mood < 5:
        score -= 15

    return max(score, 0)