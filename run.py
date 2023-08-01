import re
from rich.console import Console
import os

from scripts.scraper import (
    load_json_data, 
    prettify_json, 
    copy_block
    )

from scripts.standings import (
    Match,
    get_standings
)

def main():
    MAIN_FOLDER = os.path.dirname(__file__)
    KICKER_FOLDER = os.path.join(MAIN_FOLDER, 'files/kicker')
    PRETTY_FOLDER = os.path.join(MAIN_FOLDER, 'files/pretified')
    SCRAPED_FOLDER = os.path.join(MAIN_FOLDER, 'files/scraped')

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
            source_data = load_json_data(source_file)
            matches = []
            eliminations = data.get("eliminations", [])
            created_at = source_data.get('createdAt')
            print('===================================')
            if created_at is not None:
                tournament_date = re.sub(r'^(\d{2})\d{2}-(\d{2})-(\d{2}).*$', r'\1-\2-\3', created_at)
                print(f'Tournament day: {tournament_date}')
            else:
                print("Tournament date key(createdAt) not found in the JSON data.")
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
