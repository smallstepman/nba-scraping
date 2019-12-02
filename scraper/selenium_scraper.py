import os
from datetime import datetime

import psycopg2
from selenium import webdriver
from bs4 import BeautifulSoup

def get_team_id(team_name):
    cur.execute('SELECT id FROM team WHERE team.name = %s', (team_name,))
    id = cur.fetchone()
    return id

def create_team_if_doesnt_exist(team_name, logo_url):
    cur.execute('SELECT * FROM team WHERE team.name = %s;', (team_name,))
    teams = cur.fetchall()
    if teams:
        return
    else:
        cur.execute('INSERT INTO team (name, logo_url) VALUES (%s, %s);',
        (team_name, logo_url))
        con.commit()

def get_logo_url(bs):
    try:
        return bs.find('img').get('src')
    except:
        return ''

souplist_to_int = lambda sl: tuple(int(soup.text) for soup in sl )

con = psycopg2.connect(os.environ.get('POSTGRES_CONNECTION_STRING')) 
cur = con.cursor()

date = datetime.strptime(os.environ.get('QUERYDATE'),'%Y-%m-%d')

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox") # Bypass OS security model
options.add_argument('--headless') # Run without GUI

driver = webdriver.Chrome(desired_capabilities=options.to_capabilities())
driver.set_window_position(0, 0)
driver.set_window_size(1024, 768)
driver.get(f"https://www.espn.com/nba/scoreboard/_/date/{date:%Y%m%d}")

html = driver.page_source
soup = BeautifulSoup(html)

for article in soup.find_all("article", {"class":"scoreboard"}):
    espn_game_id = article['id']

    home_team = article.find('tr', {"class":["home"]})
    home_logo_url = get_logo_url(home_team)
    home_team_fullname = home_team.find('span', {'class':'sb-team-short'}).text
    home_team_scores = souplist_to_int(home_team.find_all('td', {'class':['score']}))
    create_team_if_doesnt_exist(home_team_fullname, home_logo_url)
    home_team_id = get_team_id(home_team_fullname)
    
    away_team = article.find('tr', {"class":["away"]})
    away_logo_url = get_logo_url(home_team)
    away_team_fullname = away_team.find('span', {'class':'sb-team-short'}).text
    away_team_scores = souplist_to_int(away_team.find_all('td', {"class":["score"]}))
    create_team_if_doesnt_exist(away_team_fullname, away_logo_url)
    away_team_id = get_team_id(away_team_fullname)
    
    cur.execute('''
    INSERT INTO game 
    (espn_game_id, date, home_team_id, away_team_id) 
    VALUES (%s, %s, %s, %s);''',
    (espn_game_id, date, home_team_id, away_team_id))

    for idx,(home,away) in enumerate(zip(home_team_scores, away_team_scores)):

        cur.execute('''
        INSERT INTO quarter_score 
        (espn_game_id, quarter_count, 
         away_team_score, home_team_score) 
        VALUES (%s, %s, %s, %s)''',
        (espn_game_id, idx+1, away, home))
        print(idx+1, away)

    con.commit()
