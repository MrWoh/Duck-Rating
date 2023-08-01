from rich.table import Table
from rich.text import Text
from rich.console import Console

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

        table.add_row("", "", "", "")

        team1_result, team2_result = self.results
        overall_result = f'{team1_result}-{team2_result}'
        overall_winner = self.get_match_winner(team1_result, team2_result)
        overall_result_row = [Text(self.team1, style="bold"), Text(f'Match result: {overall_result}', style="bold"), Text(self.team2, style="bold"), Text(f'Overall Winner: {overall_winner}', style="bold")]
        table.add_row(*overall_result_row, style="yellow")

        console = Console()
        console.print(table)

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