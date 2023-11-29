import util

def calculate_ratios(db_filename, table_name, txt_filename):
    cur, conn = util.connect_to_database(db_filename)

    cur.execute(f'SELECT home_name FROM {table_name}')
    team_list = list(set([team[0] for team in cur.fetchall()])) # remove duplicates

    for index, team in enumerate(team_list):
        cur.execute(f'SELECT * FROM {table_name} WHERE home_name = "{team}" AND home_score > away_score')
        home_wins = len(cur.fetchall())
        
        cur.execute(f'SELECT * FROM {table_name} WHERE home_name = "{team}" AND home_score < away_score')
        home_losses = len(cur.fetchall())

        cur.execute(f'SELECT * FROM {table_name} WHERE away_name = "{team}" AND away_score > home_score')
        away_wins = len(cur.fetchall())
        
        cur.execute(f'SELECT * FROM {table_name} WHERE away_name = "{team}" AND away_score < home_score')
        away_losses = len(cur.fetchall())

        # ignore ties
        home_win_percentage = 0.0
        if (home_wins + home_losses) != 0:
            home_win_percentage = home_wins / (home_wins + home_losses)

        away_win_percentage = 0.0
        if (away_wins + away_losses) != 0:
            away_win_percentage = away_wins / (home_wins + home_losses)

        team_list[index] = (team, home_win_percentage, away_win_percentage)

    top5_home_teams = sorted(team_list, key = lambda t : t[1])[-5:]
    top5_away_teams = sorted(team_list, key = lambda t : t[2])[-5:]
    
    file = open(txt_filename, 'w')

    file.write('--- Top 5 Home Win Percentages ---\n')
    for team, home_win_percentage, away_win_percentage in top5_home_teams:
        file.write(f'{team} {round(home_win_percentage, 3)}\n')

    file.write('--- Top 5 Away Win Percentages ---\n')
    for team, home_win_percentage, away_win_percentage in top5_away_teams:
        file.write(f'{team} {round(away_win_percentage, 3)}\n')
    
    file.close()
    conn.commit()
    

def visualize(txt_filename):
    # TODO
    pass

def average_visualize():
    # TODO
    pass