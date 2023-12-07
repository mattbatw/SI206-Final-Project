import os 
import sqlite3
import requests

from bs4 import BeautifulSoup


game_headers = ['game_id    INTEGER PRIMARY KEY',
                'home_id    INTEGER', 
                'away_id    INTEGER', 
                'home_score INTEGER', 
                'away_score INTEGER']

name_headers = ['id INTEGER PRIMARY KEY',
                'name TEXT']


def store_to_db(table_name, headers, rows, limit=3):
    """
    Stores rows into the database. 
    Limited to 3 rows per call by default.

    Parameters
    -----------------------
    table_name: string
        The table to add to.

    headers: list
        The headers of the table.

    rows: list
        A list of tuples where every tuple is a row of data.

    Returns
    -----------------------
    None
    """

    # Connect to database
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/sports.db")
    cur = conn.cursor()
    
    # Insert a max of (limit) rows into the table
    
    cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(headers)})')

    old_size = cur.execute(f'SELECT COUNT(*) FROM {table_name}').fetchone()[0]
    
    for row in rows: 
        cur.execute(f'INSERT OR IGNORE INTO {table_name} VALUES ({", ".join(["?"] * len(headers))})', row)
        
        new_size = cur.execute(f'SELECT COUNT(*) FROM {table_name}').fetchone()[0]
        if new_size - old_size >= limit:
            break
        
    conn.commit()


def populate_baseball_tables():
    """
    Calls Baseball API and extracts useful data. 
    Uses store_to_db() to store the result. 

    Parameters
    -----------------------
    None

    Returns
    -----------------------
    None
    """

    # Call API
    
    url = 'https://statsapi.mlb.com/api/v1/schedule'
    params = {
      'sportId'   : '1',
      'startDate' : '01/01/2022',
      'endDate'   : '4/6/2022',
      'fields'    : 'dates,games,gamePk,officialDate,teams,score,team,name'
    }
    response = requests.get(url, params)

    # Extract data
     
    game_rows = []
    name_dict = {}
    game_id = 1
    name_id = 1

    for date in response.json()['dates']:
        for game in date['games']:
            home_info = game['teams']['home']
            away_info = game['teams']['away']
            
            if 'score' not in home_info:
                continue # Some games got cancelled
            
            home_name = home_info['team']['name']
            away_name = away_info['team']['name']
            home_score = home_info['score']
            away_score = away_info['score']
            
            if home_name not in name_dict:
                name_dict[home_name] = name_id
                name_id += 1

            if away_name not in name_dict:
                name_dict[away_name] = name_id
                name_id += 1

            game_rows.append((game_id, name_dict[home_name], name_dict[away_name], home_score, away_score))
            game_id += 1

    name_rows = [(id, name) for name, id in name_dict.items()]

    # Store data
    
    store_to_db('baseball_games',      game_headers, game_rows)
    store_to_db('baseball_team_names', name_headers, name_rows)


def populate_basketball_tables():
    """
    Calls Basketball API and extracts useful data. 
    Uses store_to_db() to store the result.  

    Parameters
    -----------------------
    None

    Returns
    -----------------------
    None
    """

    # Call API
    
    url = 'https://www.balldontlie.io/api/v1/games'
    params = {
        'season': '2022',
        'per_page': '100'
    }
    response = requests.get(url, params)

    # Extract data
    
    game_rows = []
    name_dict = {}
    game_id = 1
    name_id = 1

    for game in response.json()['data']:
        home_name = game['home_team']['full_name']
        away_name = game['visitor_team']['full_name']
        home_score = game['home_team_score']
        away_score = game['visitor_team_score']

        if home_name not in name_dict:
                name_dict[home_name] = name_id
                name_id += 1

        if away_name not in name_dict:
            name_dict[away_name] = name_id
            name_id += 1

        game_rows.append((game_id, name_dict[home_name], name_dict[away_name], home_score, away_score))
        game_id += 1
        
    name_rows = [(id, name) for name, id in name_dict.items()]

    # Store data
    
    store_to_db('basketball_games',      game_headers, game_rows)
    store_to_db('basketball_team_names', name_headers, name_rows)


def populate_football_tables():
    """
    Calls Football BeautifulSoup and extracts useful data. 
    Uses store_to_db() to store the result. 

    Parameters
    -----------------------
    None

    Returns
    -----------------------
    None
    """
    
    # Request Website and Create Soup
    
    url = "https://www.thesportsdb.com/season/4391-NFL/2022&all=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract data
    
    game_rows = []
    name_dict = {}
    game_id = 1
    name_id = 1
    
    for _, tr in enumerate(soup.find_all('tr')):
        td_list = tr.find_all('td')

        if len(td_list) < 6:
            continue

        home_name = td_list[3].text.strip()
        away_name = td_list[5].text.strip()
        home_score, _, away_score = td_list[4].text.split()
        home_score = int(home_score)
        away_score = int(away_score)

        if home_name not in name_dict:
                name_dict[home_name] = name_id
                name_id += 1

        if away_name not in name_dict:
            name_dict[away_name] = name_id
            name_id += 1

        game_rows.append((game_id, name_dict[home_name], name_dict[away_name], home_score, away_score))
        game_id += 1
        
    name_rows = [(id, name) for name, id in name_dict.items()]

    # Store data
    
    store_to_db('football_games',      game_headers, game_rows)
    store_to_db('football_team_names', name_headers, name_rows)


def populate_soccer_tables():
    """
    Calls Soccer API and extracts useful data. 
    Uses store_to_db() to store the result. 

    Parameters
    -----------------------
    None

    Returns
    -----------------------
    None
    """
    
    # Call API
    
    url = 'https://api.openligadb.de/getmatchdata/bl1/2022'
    response = requests.get(url)

    # Extract data
    
    game_rows = []
    name_dict = {}
    game_id = 1
    name_id = 1

    for game in response.json():
        home_name = game['team1']['teamName']
        away_name = game['team2']['teamName']
        home_score = game['matchResults'][0]['pointsTeam1']
        away_score = game['matchResults'][0]['pointsTeam2']

        if home_name not in name_dict:
                name_dict[home_name] = name_id
                name_id += 1

        if away_name not in name_dict:
            name_dict[away_name] = name_id
            name_id += 1

        game_rows.append((game_id, name_dict[home_name], name_dict[away_name], home_score, away_score))
        game_id += 1

    name_rows = [(id, name) for name, id in name_dict.items()]

    # Store data
    
    store_to_db('soccer_games',      game_headers, game_rows)
    store_to_db('soccer_team_names', name_headers, name_rows)
        