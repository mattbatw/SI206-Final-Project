import os
import sqlite3
import matplotlib.pyplot as plt 


def calculate_ratios(sport):
    """
    Selects SPECIFIC sport data from the database, calculates the home/away win percentages for each team, and writes the result to a text file.

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

    # Generate list of unique teams
    
    cur.execute(f'SELECT home_name FROM {sport}')
    home_team_col = cur.fetchall()

    cur.execute(f'SELECT away_name FROM {sport}')
    away_team_col = cur.fetchall()

    team_list = home_team_col + away_team_col
    team_list = list(set([team[0] for team in team_list])) # Trick to remove duplicates

    # Calculate home win % and away win % for each team
    # Note: Ignores ties
    
    for index, team in enumerate(team_list):
        cur.execute(f'SELECT * FROM {sport} WHERE home_name = "{team}" AND home_score > away_score')
        home_wins = len(cur.fetchall())
        
        cur.execute(f'SELECT * FROM {sport} WHERE home_name = "{team}" AND home_score < away_score')
        home_losses = len(cur.fetchall())

        cur.execute(f'SELECT * FROM {sport} WHERE away_name = "{team}" AND away_score > home_score')
        away_wins = len(cur.fetchall())
        
        cur.execute(f'SELECT * FROM {sport} WHERE away_name = "{team}" AND away_score < home_score')
        away_losses = len(cur.fetchall())

        home_win_percentage = 0
        if (home_wins + home_losses) != 0:
            home_win_percentage = (100 * home_wins) // (home_wins + home_losses)

        away_win_percentage = 0
        if (away_wins + away_losses) != 0:
            away_win_percentage = (100 * away_wins) // (away_wins + away_losses)

        team_list[index] = (team, home_win_percentage, away_win_percentage)

    # Find the top 5 home teams and away teams
    
    top5_home_teams = sorted(team_list, key = lambda t : t[1], reverse=True)[:5]
    top5_away_teams = sorted(team_list, key = lambda t : t[2], reverse=True)[:5]
    
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
    Reads the text file and creates a bar graph visualization for the top 5 home/away win percentages.

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
    Creates a scatter plot visualization for the home/away points scored on each date for baseball.

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

    # Generate list of dates and scores
    
    cur.execute(f"""SELECT baseball_dates.date, baseball.home_score, baseball.away_score
                    FROM baseball JOIN baseball_dates ON baseball.id = baseball_dates.id""")

    data = []

    for date, home_score, away_score in cur.fetchall():
        date = date[5:] # Don't need "2022-" at the start
        score = int(home_score) + int(away_score)
        data.append((date, score))

    data.sort(key= lambda t : int(t[0].replace('-', '')))

    dates = []
    scores = []

    for date, score in data:
        dates.append(date)
        scores.append(score)

    # Create scatter plot
    
    plt.title('Points Scored in Baseball Games in 2022')
    plt.xlabel("Date", color='gray')  
    plt.ylabel("Points", color='gray')  
    
    plt.scatter(dates, scores, color='#6932a8', label='Game')
    plt.xticks(rotation=45, ha='right')

    plt.legend()
    plt.tight_layout()
    plt.show()