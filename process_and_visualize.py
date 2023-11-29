import util
import matplotlib.pyplot as plt 


def calculate_ratios(db_filename, sport):
    """
    Selects data from the database, calculates the home/away win percentages for each team, and writes the result to a text file.

    Parameters
    -----------------------
    db_filename: string
        The database file to use.

    sport: string
        The sport to calculate percentages for.

    Returns
    -----------------------
    None
    """
    
    cur, conn = util.connect_to_database(db_filename)

    cur.execute(f'SELECT home_name FROM {sport}')
    home_team_col = cur.fetchall()

    cur.execute(f'SELECT away_name FROM {sport}')
    away_team_col = cur.fetchall()

    team_list = home_team_col + away_team_col
    team_list = list(set([team[0] for team in team_list])) # remove duplicates

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

    top5_home_teams = sorted(team_list, key = lambda t : t[1], reverse=True)[:5]
    top5_away_teams = sorted(team_list, key = lambda t : t[2], reverse=True)[:5]
    
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
    Reads the text file and creates a visualization for the top 5 home/away win percentages.

    Parameters
    -----------------------
    sport: string
        The sport to create a visualization for.

    Returns
    -----------------------
    None
    """

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
    plt.show()


def calculate_average_ratio(db_filename):
    """
    Selects data from the database, calculates the average home/away win percentages for each sport, and writes the result to totals.txt.

    Parameters
    -----------------------
    db_filename: string
        The database file to use.

    Returns
    -----------------------
    None
    """
    
    pass

def average_visualize():
    """
    Reads totals.txt and creates a visualization for the average home/away win percentages per sport.

    Parameters
    -----------------------
    None

    Returns
    -----------------------
    None
    """

    home_data = {}
    away_data = {}

    sports = ['baseball', 'basketball', 'football', 'soccer']

    for sport in sports:
        file = open(f'{sport}.txt', 'r')

        home_total = 0
        away_total = 0
        
        file.readline()
        for _ in range(5):
            line = file.readline()
            home_total += int(line.split()[-1])

        home_data[sport] = home_total / len(sports)

        file.readline()
        for _ in range(5):
            line = file.readline()
            away_total += int(line.split()[-1])

        away_data[sport] = away_total / len(sports)

        file.close()

    home_sport_names = list(home_data.keys())
    home_averages = list(home_data.values())

    away_sport_names = list(away_data.keys())
    away_averages = list(away_data.values())

    fig, axs = plt.subplots(2, figsize=(10, 5))
    fig.suptitle(f'Average Home & Away Win Percentages in 2022 \n *only top 5 percentages per sport included')

    axs[0].bar(home_sport_names, home_averages, color='#32a879', width=0.4)
    axs[1].bar(away_sport_names, away_averages, color='#4bb8e3', width=0.4)

    axs[0].set_ylabel("Average Home Win Rate (%)", color='gray')  
    axs[1].set_ylabel("Average Away Win Rate (%)", color='gray')

    axs[0].set_ylim(0, 100) 
    axs[1].set_ylim(0, 100)

    axs[0].set_xlabel("Sport", color='gray')
    axs[1].set_xlabel("Sport", color='gray')

    for i, value in enumerate(home_averages):
        axs[0].text(i, value + 2, str(value), ha='center', va='bottom')

    for i, value in enumerate(away_averages):
        axs[1].text(i, value + 2, str(value), ha='center', va='bottom')

    plt.subplots_adjust(hspace=0.6)   
    plt.show()
        
        