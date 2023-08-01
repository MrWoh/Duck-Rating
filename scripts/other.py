import re

def get_tournament_date(date_string):
    return re.sub(r'^(\d{2})\d{2}-(\d{2})-(\d{2}).*$', r'\1-\2-\3', date_string)

def get_category(total_points):
    if total_points >= 50:
        return "Master"
    elif total_points >= 40:
        return "Pro"
    elif total_points >= 30:
        return "Semi-Pro"
    elif total_points >= 20:
        return "Amateur"
    elif total_points >= 10:
        return "Novice"
    else:
        return "Beginner"