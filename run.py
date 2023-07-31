import json
import os
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel

class Match:
    def __init__(self, team1, team2, sets_list, results):
        self.team1 = team1 or 'Team 1 Unknown'
        self.team2 = team2 or 'Team 2 Unknown'
        self.sets_list = sets_list
        self.results = results
        
    def get_match_winner(self, team1_score, team2_score):
        if team1_score > team2_score:
            return self.team1
        elif team1_score < team2_score:
            return self.team2
        else:
            return "Tie"

    def print_match_results(self):
        print('''
=========================================================================================================
              ''')
        table = Table(title=f"Match Results - {self.team1} vs. {self.team2}", show_header=False, border_style="bright_black")
        table.add_column("Team 1", justify="right", style="cyan")
        table.add_column("Score", style="cyan", justify="center")
        table.add_column("Team 2", justify="left", style="cyan")
        table.add_column("Winner", style="magenta", no_wrap=True)

        for set_info in self.sets_list:
            scores = set_info.get('scores', 'Scores Unknown')
            team1_score, team2_score = scores
            winner = self.get_match_winner(team1_score, team2_score)

            table.add_row(self.team1, Text(f'{team1_score}-{team2_score}', style="bold"), self.team2, winner)

        # Add a separator between sets and overall result
        table.add_row("", "", "", "")

        # Add a row to display the overall match result for team1 and team2 with row highlighting
        team1_result, team2_result = self.results
        overall_result = f'{team1_result}-{team2_result}'
        overall_winner = self.get_match_winner(team1_result, team2_result)
        overall_result_row = [Text(self.team1, style="bold"), Text(f'Match result: {overall_result}', style="bold"), Text(self.team2, style="bold"), Text(f'Overall Winner: {overall_winner}', style="bold")]
        table.add_row(*overall_result_row, style="yellow")

        console = Console()
        console.print(table)

def load_json_data(file_path):
    with open(file_path, "r") as json_file:
        return json.load(json_file)

def prettify_json(input_file_path, output_file_path):
    with open(input_file_path, 'r') as json_file:
        json_object = json.load(json_file)
    
    with open(output_file_path, 'w') as write_file:
        json.dump(json_object, write_file, indent=4, sort_keys=True)

def copy_block(source_file, target_file, block_name):
    with open(source_file, 'r') as source:
        source_data = json.load(source)

    if block_name in source_data:
        block_to_copy = source_data[block_name]
    else:
        print(Panel(f"The block '{block_name}' does not exist in the source file."))
        return

    with open(target_file, 'w') as target:
        json.dump({block_name: block_to_copy}, target, indent=4)

def calculate_points(position_str):
    position = int(position_str)
    points_mapping = {
        1: 50,
        2: 40,
        3: 32,
        4: 24,
        5: 16,
    }
    return points_mapping.get(position, 8)

def get_standings(data):
    standings_table = Table(title="Eliminations Standings")
    standings_table.add_column("Player Name", style="cyan", justify="right")
    standings_table.add_column("Place", style="magenta")
    standings_table.add_column("Goals", style="yellow")
    standings_table.add_column("Goals In", style="yellow")
    standings_table.add_column("Points", style="green")

    eliminations = data.get("eliminations", [])
    for elimination in eliminations:
        standings = elimination.get("standings", [])
        for player_data in standings:
            player_name = player_data.get("name", "Player Name Unknown")
            place_str = str(player_data.get("stats").get("place", "Place Unknown"))
            goals = str(player_data.get("stats").get("goals", "Goals Unknown"))
            goals_in = str(player_data.get("stats").get("goals_in", "Goals In Unknown"))
            points = str(calculate_points(place_str))  # Convert points to a string
            standings_table.add_row(player_name, place_str, goals, goals_in, points)

    return standings_table

def main():
    MAIN_FOLDER = os.path.dirname(__file__)
    KICKER_FOLDER = os.path.join(MAIN_FOLDER, 'kicker')
    PRETTY_FOLDER = os.path.join(MAIN_FOLDER, 'pretified')
    SCRAPED_FOLDER = os.path.join(MAIN_FOLDER, 'scraped')

    # Prettify JSON files in KICKER_FOLDER and store in PRETTY_FOLDER
    for file in os.listdir(KICKER_FOLDER):
        input_file_path = os.path.join(KICKER_FOLDER, file)
        output_file_path = os.path.join(PRETTY_FOLDER, file)

        if os.path.isfile(input_file_path) and not os.path.exists(output_file_path):
            prettify_json(input_file_path, output_file_path)
            print(f'Refactored {file}')
            print('===================================')
        elif os.path.exists(output_file_path):
            print(f"Skipping {file} as the prettified version already exists.")
            print('===================================')

    # Iterate through PRETTY_FOLDER and copy 'eliminations' block to SCRAPED_FOLDER
    for filename in os.listdir(PRETTY_FOLDER):
        if filename.endswith('.json'):
            source_file = os.path.join(PRETTY_FOLDER, filename)
            target_file = os.path.join(SCRAPED_FOLDER, filename)
            if not os.path.exists(target_file):
                copy_block(source_file, target_file, 'eliminations')
                print(f'Scraped eliminations from {filename}.')
                print('===================================')
            else:
                print(f'Skipping scraping for {filename} as the file already exists.')
                print('===================================')

            # Load data and print scores for the scraped file
            data = load_json_data(target_file)
            matches = []
            eliminations = data.get("eliminations", [])
            if eliminations:
                levels = eliminations[0].get("levels", [])
                for level in levels:
                    matches.extend(level.get("matches", []))
            for match in matches:
                team1 = match['team1'].get('name') if match['team1'] else None
                team2 = match['team2'].get('name') if match['team2'] else None
                sets_list = match.get('disciplines', [])[0].get('sets', [])
                results = match.get('result', 'Results Unknown')
                current_match = Match(team1, team2, sets_list, results)
                current_match.print_match_results()
            print()

            # Get and display standings table
            standings_table = get_standings(data)
            console = Console()
            console.print(standings_table)

if __name__ == "__main__":
    main()
