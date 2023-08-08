#!/usr/bin/env -S poetry run python
from rich.console import Console
import os

from scripts.other import get_tournament_date

from scripts.scraper import (
    load_json_data, 
    prettify_json, 
    copy_block
    )

from scripts.standings import (
    Match,
    get_standings,
)

from scripts.get_csv import (
    get_standings_dataframe
)

def main():
    tables = False
    standings = False
    MAIN_FOLDER = os.path.dirname(__file__)
    KICKER_FOLDER = os.path.join(MAIN_FOLDER, 'files/kicker')
    PRETTY_FOLDER = os.path.join(MAIN_FOLDER, 'files/pretified')
    SCRAPED_FOLDER = os.path.join(MAIN_FOLDER, 'files/scraped')

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

            data = load_json_data(target_file)
            source_data = load_json_data(source_file)
            tournament_date = get_tournament_date(source_data.get('createdAt'))
            if tables:
                print(f'Tournament day: {tournament_date}')
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
                print('===================================')
            else:
                print('Table printing disabled')
                print('===================================')

            if standings:
                standings_table = get_standings(data)
                console = Console()
                console.print(standings_table)
                print('===================================')
            else:
                print('Standings printing disabled')
                print('===================================')
            
            get_standings_dataframe(data)

if __name__ == "__main__":
    main()