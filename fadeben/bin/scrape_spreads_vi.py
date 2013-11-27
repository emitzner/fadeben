"""
If there's games going on right now, lets try and see if they're over by grabbing the scores from NFL's site
"""
import sys
import logging
import os
import urllib2

from bs4 import BeautifulSoup

from fadeben import api

from fadeben.model import Session, Team

from pylons import app_globals as g

log = logging.getLogger("fadeben.spread_scraper_vi")

TEAM_MAP = {
    "BUF": "BUF",
    "WAS": "WAS",
    "NYJ": "NYJ",
    "NYG": "NYG",
    "CLE": "CLE",
    "IND": "IND",
    "PHI": "PHI",
    "JAC": "JAC",
    "KAN": "KC",
    "PIT": "PIT",
    "TAM": "TB",
    "MIA": "MIA",
    "STL": "STL",
    "DEN": "DEN",
    "CIN": "CIN",
    "DAL": "DAL",
    "ATL": "ATL",
    "TEN": "TEN",
    "SDC": "SD",
    "ARI": "ARI",
    "NOS": "NO",
    "HOU": "HOU",
    "MIN": "MIN",
    "SFO": "SF",
    "BAL": "BAL",
    "CHI": "CHI",
    "CAR": "CAR",
    "SEA": "SEA",
    "OAK": "OAK",
    "DET": "DET",
    "NEP": "NE",
    "GBP": "GB",
}

def normalize_and_find(name):
    abbr = TEAM_MAP[name]
    return Session.query(Team).filter(Team.abbr==abbr).one()

def parse_li_data(data):
    raw_team_data = str(data.find("span", class_="team-abbr").string)
    raw_spread_data = str(data.find("span", class_="column-open").string)
    team = normalize_and_find(raw_team_data)
    return {'team': team, 'spread_value': raw_spread_data}

def get_spread(raw_home_spread, raw_away_spread):
    stripped_home_spread = raw_home_spread.split(" ")[0]
    stripped_away_spread = raw_away_spread.split(" ")[0]

    if stripped_home_spread.strip() == 'PK':
        return 0.0
    elif stripped_away_spread.strip() == 'PK':
        return 0.0

    try:
        abs_value_ats = abs(float(stripped_away_spread))
    except TypeError as e:
        return float(stripped_home_spread)

    try:
        abs_value_hts = abs(float(stripped_home_spread))
    except TypeError as e:
        return float(stripped_away_spread)


    if abs_value_ats > abs_value_hts:
        spread_value = float(stripped_home_spread)
    else:
        spread_value = float(stripped_away_spread)

    return spread_value
    

def normalize_game_data(raw_data):
    normalized = []
    for game_id in raw_data:
        game_data = raw_data[game_id]

        spread = get_spread(game_data['home_team_data']['spread_value'],
                            game_data['away_team_data']['spread_value'])

        normalized.append({
            'home_team': game_data['home_team_data']['team'],
            'away_team': game_data['away_team_data']['team'],
            'spread': spread
        })

    return normalized

def scrape_spreads():
    current_season = g.serverconfig.get_value('current_season')
    current_week = api.nfl.season.current_week(season=current_season)

    games = api.nfl.game.list(season=current_season, week=current_week, no_spread=True)

    if not games:
        log.info("No games need their spreads")
        return

    games_data = {}

    try:
        raw_data = urllib2.urlopen("http://m.vegasinsider.com/thisweek/3/NFL").read()
    except socket.timeout:
        log.error("Socket timeout when trying to scrape vegas insiders site. Exiting")
        return

    soup_data = BeautifulSoup(raw_data)

    home_team_lis = soup_data.find_all('li', class_="home-team")
    away_team_lis = soup_data.find_all('li', class_="away-team")

    # loop over the home team li's and store the game ids.
    for htl in home_team_lis:
        game_id = int(htl.attrs['data-game-id'])
        games_data[game_id] = {
            'home_team_data': parse_li_data(htl),
        }

    # now loop over hte away team li's as well
    for atl in away_team_lis:
        game_id = int(atl.attrs['data-game-id'])
        games_data[game_id]['away_team_data'] = parse_li_data(atl)

    # now we've got a dict of game data.  we need to go through
    # and normalize it so we've got spreads relative to the home
    # team.
    normalized_game_data = normalize_game_data(games_data)

    # we've now got the normalized game data.
    # let's go ahead and find the game in the database and
    # update it with the spread.
    
    counter = 0

    for game in games:
        # find the corresponding entry in the normalized game data
        for gd in normalized_game_data:
            sm = None
            if game.home_team_id == gd['home_team'].id:
                sm = gd
                break

        if sm is None:
            log.info("No spread found for game {0}".format(game.short_display()))
            continue

        if game.away_team_id != sm['away_team'].id:
            log.warn("Spread found for game {0} with matching home team, but mismatched away team! Spread data: {1}".format(
                game.short_display(), sm
            )
            )
            continue

        log.info("Found spread for {0}. Updating record with spread {1}".format(
            game.short_display(),
            sm['spread']
        ))

        game.spread = sm['spread']
        Session.add(game)
        counter += 1
        

    Session.commit()
    log.info("Updated {0} games with their spreads".format(counter))

if __name__ == '__main__':
    import fadeben.lib.bootstrap
    scrape_spreads()
