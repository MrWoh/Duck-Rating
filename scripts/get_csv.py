import os
import pandas as pd

from scripts.other import get_tournament_date, get_category
from scripts.standings import calculate_points
from scripts.scraper import load_json_data

def get_standings_dataframe(data):
    player_data_dict = {}
    MAIN_FOLDER = os.path.dirname(__file__)
    PRETTY_FOLDER = os.path.join(MAIN_FOLDER, '../files/pretified')
    CSV_FOLDER = os.path.join(MAIN_FOLDER, '../files/csv')

    for filename in os.listdir(PRETTY_FOLDER):
        if filename.endswith('.json'):
            source_file = os.path.join(PRETTY_FOLDER, filename)
            source_data = load_json_data(source_file)
            tournament_date = get_tournament_date(source_data.get('createdAt'))
            eliminations = source_data.get("eliminations", [])
            for elimination in eliminations:
                standings = elimination.get("standings", [])
                for player_data in standings:
                    player_name = player_data.get("name", "Player Name Unknown")
                    place_str = str(player_data.get("stats").get("place", "Place Unknown"))
                    points = calculate_points(place_str)

                    if player_name not in player_data_dict:
                        player_data_dict[player_name] = {
                            "Player Name": player_name,
                            "Total": 0,
                        }

                    player_data_dict[player_name][f"{tournament_date}"] = points
                    player_data_dict[player_name]["Total"] += points

    player_data_list = list(player_data_dict.values())
    standings_df = pd.DataFrame(player_data_list)

    standings_df["Category"] = standings_df["Total"].apply(get_category)

    csv_file_path = os.path.join(CSV_FOLDER + "/standings.csv")
    if os.path.exists(csv_file_path):
        existing_standings_df = pd.read_csv(csv_file_path, index_col=0)

        standings_df.set_index("Player Name", inplace=True)
        existing_standings_df.update(standings_df)
        standings_df = existing_standings_df.reset_index()

    standings_df.to_csv(csv_file_path, index=False)
    print('Data exported')
    print('===================================')

    return standings_df




