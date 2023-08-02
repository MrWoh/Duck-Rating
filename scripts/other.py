import re
import pandas as pd
import os

def get_tournament_date(date_string):
    return re.sub(r'^(\d{2})\d{2}-(\d{2})-(\d{2}).*$', r'\1-\2-\3', date_string)

def get_category(total_points):
    if total_points >= 120:
        return "Master"
    elif total_points >= 90:
        return "Pro"
    elif total_points >= 70:
        return "Semi-Pro"
    elif total_points >= 50:
        return "Intermediate"
    elif total_points >= 20:
        return "Amateur"
    else:
        return "Novice"
    
def validate_name(player_name):
    name_options = {
        "JohnDoe": ["John", "JohnDoe"],
        "JaneSmith": ["Jane", "JaneSmith"]
    }

    for valid_name, name_variants in name_options.items():
        if player_name in name_variants:
            return valid_name

    return player_name

def associate_emails_to_names_in_csv(email_name_mapping):
    MAIN_FOLDER = os.path.dirname(__file__)
    CSV_FOLDER = os.path.join(MAIN_FOLDER, '../files/csv')

    csv_file_path = os.path.join(CSV_FOLDER, "standings.csv")
    if not os.path.isfile(csv_file_path):
        print('No files found, skipping')
        return
    standings_df = pd.read_csv(csv_file_path)

    for name, email in email_name_mapping.items():
        mask = standings_df["Player Name"] == name
        standings_df.loc[mask, "Email"] = email

    standings_df.to_csv(csv_file_path, index=False)

email_name_mapping = {
    "JohnDoe": "john@example.com",
    "JaneSmith": "jane@example.com"
}

associate_emails_to_names_in_csv(email_name_mapping)