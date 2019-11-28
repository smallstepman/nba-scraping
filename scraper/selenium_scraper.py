import os
from datetime import datetime, date

import psycopg2
from selenium import webdriver
from bs4 import BeautifulSoup
cs = "dbname=qzejnvqh user=qzejnvqh password=JwXyIlpv2oCl-seP1Q6u4lAHQcmc5Gvo host=rogue.db.elephantsql.com port=5432" 
con = psycopg2.connect(os.environ['POSTGRES_CONNECTION_STRING']) 
cur = con.cursor()

env_date = os.environ.get('QUERYDATE', '2019-10-10')
day = datetime.strptime(env_date,'%Y-%m-%d')

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox") # Bypass OS security model
options.add_argument('--headless') # Run without GUI

driver = webdriver.Chrome(desired_capabilities=options.to_capabilities())
driver.get(f"https://www.espn.com/nba/scoreboard/_/date/{day:%Y%m%d}")

html = driver.page_source
soup = BeautifulSoup(html)

souplist_to_int = lambda sl: tuple(int(soup.text) for soup in sl )

for article in soup.find_all("article", {"class":"scoreboard"}):
    espn_game_id = article['id']
    
    home_team = article.find('tr', {"class":["home"]})
    away_team = article.find('tr', {"class":["away"]})
    
    home_team_fullname = home_team.find('span', {'class':'sb-team-short'}).text
    home_team_abbrev = home_team.find('span', {'class':'sb-team-abbrev'}).text
    home_team_scores = souplist_to_int(home_team.find_all('td', {'class':['score']}))
    
    away_team_fullname = away_team.find('span', {'class':'sb-team-short'}).text
    away_team_abbrev = away_team.find('span', {'class':'sb-team-abbrev'}).text
    away_team_scores = souplist_to_int(away_team.find_all('td', {"class":["score"]}))
    
    cur.execute('''
    INSERT INTO game 
    (espn_game_id, date, home_team, away_team) 
    VALUES (%s, %s, %s, %s);''',
    (espn_game_id, day, home_team_fullname, away_team_fullname))
    
    for idx,(home,away) in enumerate(zip(home_team_scores, away_team_scores)):

        cur.execute('''
        INSERT INTO quarter_score 
        (espn_game_id, quarter_count, 
         away_team_score, home_team_score) 
        VALUES (%s, %s, %s, %s)''',
        (espn_game_id, idx+1, away, home))

    con.commit()



