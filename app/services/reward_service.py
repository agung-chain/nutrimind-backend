def calculate_reward(data):

    points = 100

    mood = data.get("mood", 0)
    sleep = data.get("sleep_hours", 0)
    stress = data.get("stress_level", 0)
    exercise = data.get("exercise_minutes", 0)

    # STRESS

    if stress >= 8:
        points -= 30
    elif stress >= 6:
        points -= 15

    # SLEEP

    if sleep < 5:
        points -= 25
    elif sleep < 7:
        points -= 10

    # MOOD

    if mood <= 3:
        points -= 20
    elif mood <= 5:
        points -= 10

    # EXERCISE BONUS

    if exercise >= 30:
        points += 10

    # LIMIT

    if points > 100:
        points = 100

    if points < 0:
        points = 0

    # BADGE

    if points >= 90:
        badge = "Elite Healthy Student"
        level = "Platinum"
        reward = "Healthy Lunch Premium"

    elif points >= 75:
        badge = "Healthy Student"
        level = "Gold"
        reward = "Healthy Snack"

    elif points >= 60:
        badge = "Active Student"
        level = "Silver"
        reward = "Fruit Package"

    else:
        badge = "Need Attention"
        level = "Bronze"
        reward = "Health Counseling"

    return {
        "health_points": points,
        "badge": badge,
        "level": level,
        "reward": reward
    }