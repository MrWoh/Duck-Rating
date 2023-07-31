import json
import os
from rich.console import Console
from rich.table import Table

def load_json_data(file_path):
    with open(file_path, "r") as json_file:
        return json.load(json_file)

def print_scores(file_name, matches_data):
    console = Console()

    for match in matches_data:
        table = Table(title=f"Match Results - {file_name}")
        table.add_column("Team 1", justify="right", style="cyan")
        table.add_column("Score", style="cyan")
        table.add_column("Team 2", justify="right", style="cyan")
        table.add_column("Winner", style="magenta", no_wrap=True)

        sets_list = match.get('disciplines', [])[0].get('sets', [])
        team1 = match['team1'].get('name', 'Team 1 Unknown')
        team2 = match['team2'].get('name', 'Team 2 Unknown')
        results = match.get('result', 'Results Unknown')

        for set_info in sets_list:
            scores = set_info.get('scores', 'Scores Unknown')
            team1_score, team2_score = scores

            # Determine the winner for the current set
            if team1_score > team2_score:
                winner = team1
            elif team1_score < team2_score:
                winner = team2
            else:
                winner = "Tie"

            table.add_row(f'{team1}', f'{team1_score}-{team2_score}', f'{team2}', f'{winner}')

        # Add a row to display the overall match result for team1 and team2
        team1_result, team2_result = results
        if team1_result > team2_result:
            overall_result = f'{team1_result}-{team2_result}'
            overall_winner = team1
        elif team1_result < team2_result:
            overall_result = f'{team1_result}-{team2_result}'
            overall_winner = team2
        else:
            overall_result = 'Tie'
            overall_winner = 'Tie'
        
        table.add_row(f'{team1}', f'Match result: {overall_result}', f'{team2}', f'Overall Winner: {overall_winner}')

        console.print(table)
        
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
        print(f"The block '{block_name}' does not exist in the source file.")
        return

    with open(target_file, 'w') as target:
        json.dump({block_name: block_to_copy}, target, indent=4)

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
        elif os.path.exists(output_file_path):
            print(f"Skipping {file} as the prettified version already exists.")

    # Iterate through PRETTY_FOLDER and copy 'eliminations' block to SCRAPED_FOLDER
    for filename in os.listdir(PRETTY_FOLDER):
        if filename.endswith('.json'):
            source_file = os.path.join(PRETTY_FOLDER, filename)
            target_file = os.path.join(SCRAPED_FOLDER, filename)
            if not os.path.exists(target_file):
                copy_block(source_file, target_file, 'eliminations')
                print(f'Scraped eliminations from {filename}.')
            else:
                print(f'Skipping scraping for {filename} as the file already exists.')

            # Load data and print scores for the scraped file
            data = load_json_data(target_file)
            matches = data.get("eliminations", [])[0].get("levels", [])[0].get("matches", [])
            print_scores(filename, matches)
            print()

if __name__ == "__main__":
    main()
