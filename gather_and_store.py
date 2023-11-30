import os 
import sqlite3
import requests

from bs4 import BeautifulSoup


def store_to_db(db_filename, table_name, headers, rows, limit=5):
    """
    Stores rows into the database. Limited to 5 rows per call.

    Parameters
    -----------------------
    db_filename: string
        The database file to use.

    headers: list
        The headers of the table.

    table_name: string
        The table to add to.

    rows: list
        A list of tuples where every tuple is a row of data.

    Returns
    -----------------------
    None
    """

    # Connect to database
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_filename)
    cur = conn.cursor()
    
    # Create table
    
    cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(headers)})')

    # Insert a max of 5 rows into the table
    
    old_size = cur.execute(f'SELECT COUNT(*) FROM {table_name};').fetchone()[0]
    
    for row in rows: 
        cur.execute(f'INSERT OR IGNORE INTO {table_name} VALUES ({", ".join(["?"] * len(headers))})', row)
        
        new_size = cur.execute(f'SELECT COUNT(*) FROM {table_name};').fetchone()[0]
        if new_size - old_size >= limit:
            break
        
    conn.commit()


def populate_baseball_table(db_filename):
    """
    Calls Baseball API, extracts useful data, and uses store_to_db() to store the result. 

    Parameters
    -----------------------
    db_filename: string
        The database file to use.

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

    # Parse data
    
    if response.ok:   
        rows = []
        date_rows = []

        for date in response.json()['dates']:
            for game in date['games']:
                id = game['gamePk']
                home_info = game['teams']['home']
                away_info = game['teams']['away']
                date = game['officialDate']
                
                if 'score' not in home_info:
                    continue # Some games got cancelled
                
                home_name = home_info['team']['name']
                away_name = away_info['team']['name']
                home_score = home_info['score']
                away_score = away_info['score']

                rows.append((id, home_name, away_name, home_score, away_score))
                date_rows.append((id, date))

        # Store data
        
        headers = ['id INTEGER PRIMARY KEY', 
                   'home_name TEXT', 
                   'away_name TEXT', 
                   'home_score INTEGER', 
                   'away_score INTEGER']
        
        store_to_db(db_filename, 'baseball', headers, rows)

        headers = ['id INTEGER PRIMARY KEY',
                   'date TEXT']
        
        store_to_db(db_filename, 'baseball_dates', headers, date_rows)

    else:
        exit(response.status_code)


def populate_basketball_table(db_filename):
    """
    Calls Basketball API, extracts useful data, and uses store_to_db() to store the result. 

    Parameters
    -----------------------
    db_filename: string
        The database file to use.

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

    # Parse data
    
    if response.ok:
        rows = []

        for game in response.json()['data']:
            id = game['id']
            home_name = game['home_team']['full_name']
            away_name = game['visitor_team']['full_name']
            home_score = game['home_team_score']
            away_score = game['visitor_team_score']

            rows.append((id, home_name, away_name, home_score, away_score))
        
        
        # Store data
        
        headers = ['id INTEGER PRIMARY KEY', 
                   'home_name TEXT', 
                   'away_name TEXT', 
                   'home_score INTEGER', 
                   'away_score INTEGER']
        
        store_to_db(db_filename, 'basketball', headers, rows)

    else:
        exit(response.status_code)


def populate_football_table(db_filename):
    """
    Creates Football BeautifulSoup, extracts useful data, and uses store_to_db() to store the result. 

    Parameters
    -----------------------
    db_filename: string
        The database file to use.

    Returns
    -----------------------
    None
    """
    
    # Request Website
    
    url = "https://www.thesportsdb.com/season/4391-NFL/2022&all=1"

    response = requests.get(url)

    # Parse data
    
    if response.ok:
        rows = []
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for id, tr in enumerate(soup.find_all('tr')):
            td_list = tr.find_all('td')

            if len(td_list) < 6:
                continue

            home_name = td_list[3].text.strip()
            away_name = td_list[5].text.strip()
            home_score, _, away_score = td_list[4].text.split()
            home_score = int(home_score)
            away_score = int(away_score)

            rows.append((id, home_name, away_name, home_score, away_score))
        
        # Store data
        
        headers = ['id INTEGER PRIMARY KEY', 
                   'home_name TEXT', 
                   'away_name TEXT', 
                   'home_score INTEGER', 
                   'away_score INTEGER']
        
        store_to_db(db_filename, 'football', headers, rows)

    else:
        exit(response.status_code)


def populate_soccer_table(db_filename):
    """
    Calls Soccer API, extracts useful data, and uses store_to_db() to store the result. 

    Parameters
    -----------------------
    db_filename: string
        The database file to use.

    Returns
    -----------------------
    None
    """
    
    # Call API
    
    url = 'https://api.openligadb.de/getmatchdata/bl1/2022'

    response = requests.get(url)

    # Collect data
    
    if response.ok:
        rows = []

        for game in response.json():
            id = game['matchID']
            home_name = game['team1']['teamName']
            away_name = game['team2']['teamName']
            home_score = game['matchResults'][0]['pointsTeam1']
            away_score = game['matchResults'][0]['pointsTeam2']

            rows.append((id, home_name, away_name, home_score, away_score))
        
        # Store data
        
        headers = ['id INTEGER PRIMARY KEY', 
                   'home_name TEXT', 
                   'away_name TEXT', 
                   'home_score INTEGER', 
                   'away_score INTEGER']
        
        store_to_db(db_filename, 'soccer', headers, rows)

    else:
        exit(response.status_code)