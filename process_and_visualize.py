import os
import sqlite3
import matplotlib.pyplot as plt 


def calculate_ratios(sport):
    """
    Selects data for a specific sport from the database, 
    calculates the home/away win percentages for each team, 
    and writes the top 5 results to a text file.

    Parameters
    -----------------------
    sport: string
        The sport to calculate percentages for.

    Returns
    -----------------------
    None
    """
    
    # Connect to database
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/sports.db")
    cur = conn.cursor()

    # Get names from names table
    
    cur.execute(f'SELECT id, name FROM {sport}_team_names')
    name_dict = {}
    for id, name in cur.fetchall():
        name_dict[name] = id

    # Calculate home/away wins percentages for each team

    team_win_percentages = []
    
    for name, id in name_dict.items():
        cur.execute(f"""SELECT * FROM {sport}_games 
                        WHERE home_id = "{id}" 
                        AND home_score > away_score""")
        home_wins = len(cur.fetchall())

        cur.execute(f"""SELECT * FROM {sport}_games 
                        WHERE home_id = "{id}" 
                        AND home_score < away_score""")
        home_losses = len(cur.fetchall())

        cur.execute(f"""SELECT * FROM {sport}_games 
                        WHERE away_id = "{id}" 
                        AND away_score > home_score""")
        away_wins = len(cur.fetchall())

        cur.execute(f"""SELECT * FROM {sport}_games 
                        WHERE away_id = "{id}" 
                        AND away_score < home_score""")
        away_losses = len(cur.fetchall())

        home_win_percentage = 0
        if (home_wins + home_losses) != 0:
            home_win_percentage = (100 * home_wins) // (home_wins + home_losses)

        away_win_percentage = 0
        if (away_wins + away_losses) != 0:
            away_win_percentage = (100 * away_wins) // (away_wins + away_losses)
        
        team_win_percentages.append((name, home_win_percentage, away_win_percentage))

    # Find the top 5 home teams and away teams
    
    top5_home_teams = sorted(team_win_percentages, key = lambda t : t[1], reverse=True)[:5]
    top5_away_teams = sorted(team_win_percentages, key = lambda t : t[2], reverse=True)[:5]
    
    # Write results to a text file
    
    file = open(f'{sport}.txt', 'w')

    file.write('--- Top 5 Home Win Percentages ---\n')
    for team, home_win_percentage, away_win_percentage in top5_home_teams:
        file.write(f'{team} {home_win_percentage}\n')

    file.write('--- Top 5 Away Win Percentages ---\n')
    for team, home_win_percentage, away_win_percentage in top5_away_teams:
        file.write(f'{team} {away_win_percentage}\n')
    
    file.close() 


def visualize(sport):
    """
    Reads the text file for a specific sport, and creates a bar graph visualization 
    for the top 5 home/away win percentages.

    Parameters
    -----------------------
    sport: string
        The sport to create a visualization for.

    Returns
    -----------------------
    None
    """

    # Parse data from text file
    
    file = open(f'{sport}.txt', 'r')

    home_data = {}
    away_data = {}

    file.readline()
    for _ in range(5):
        line = file.readline()

        words = line.split()
        team_name = ' '.join(words[:-1])
        percent = int(words[-1])

        home_data[team_name] = percent

    file.readline()
    for _ in range(5):
        line = file.readline()

        words = line.split()
        team_name = ' '.join(words[:-1])
        percent = int(words[-1])

        away_data[team_name] = percent

    file.close()

    # Create bar charts for home and away

    home_team_names = list(home_data.keys())
    home_percentages = list(home_data.values())

    away_team_names = list(away_data.keys())
    away_percentages = list(away_data.values())

    fig, axs = plt.subplots(2, figsize=(10, 5))
    fig.suptitle(f'Top 5 Home & Away Win Percentages for {sport.capitalize()} in 2022')

    axs[0].bar(home_team_names, home_percentages, color='#32a879', width=0.4)
    axs[1].bar(away_team_names, away_percentages, color='#4bb8e3', width=0.4)

    axs[0].set_ylabel("Home Win Rate (%)", color='gray')  
    axs[1].set_ylabel("Away Win Rate (%)", color='gray')

    axs[0].set_ylim(0, 100) 
    axs[1].set_ylim(0, 100)

    axs[0].set_xlabel("Team Name", color='gray')
    axs[1].set_xlabel("Team Name", color='gray')

    for i, value in enumerate(home_percentages):
        axs[0].text(i, value + 2, str(value), ha='center', va='bottom')

    for i, value in enumerate(away_percentages):
        axs[1].text(i, value + 2, str(value), ha='center', va='bottom')

    plt.subplots_adjust(hspace=0.6)
    plt.tight_layout()   
    plt.show()


def extra_visualization():
    """
    For baseball only, creates a bar chart visualization 
    for the maximum runs scored in a home game.

    Parameters
    -----------------------
    None

    Returns
    -----------------------
    None
    """
    
    # Connect to database
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/sports.db")
    cur = conn.cursor()

    # Get max home score for each team
    
    max_home_scores = []
    
    cur.execute('SELECT name FROM baseball_team_names')

    for name_tup in cur.fetchall():
        name = name_tup[0]
        cur.execute(f"""
            SELECT n.name, g.home_score 
            FROM baseball_games g JOIN baseball_team_names n
            ON n.id = g.home_id
            WHERE n.name = "{name}"
            AND g.home_score = (
            SELECT MAX(home_score) FROM baseball_games
            WHERE home_id = n.id)  
        """)

        res = cur.fetchone()
        if res is None:
            continue
        else:
            max_home_scores.append(res)

    max_home_scores.sort(key = lambda t : t[1])

    # Create bar chart

    teams  = list([item[0] for item in max_home_scores])
    scores = list([item[1] for item in max_home_scores])
    
    fig = plt.figure(figsize = (10, 6))
    plt.bar(teams, scores, color ='red', width = 0.4)
    
    for i, score in enumerate(scores):
        plt.text(i, score + 0.1, str(score), ha='center', va='bottom')
    
    plt.xlabel("Team", color='gray')
    plt.ylabel("Runs", color='gray')
    plt.title("The Highest Number of Runs Scored in a Home Game in 2022")
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    

    