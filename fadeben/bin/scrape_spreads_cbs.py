"""
If we've got games this week without spreads, check the CBS site to see if they've got a
spread for the game.
"""
import sys
import logging
import os
import urllib2

from bs4 import BeautifulSoup

from fadeben import api

from fadeben.model import Session, Team

from pylons import app_globals as g

log = logging.getLogger("fadeben.spread_scraper_cbs")

TEAM_MAP = {
    "Bills": "BUF",
    "Redskins": "WAS",
    "Jets": "NYJ",
    "Giants": "NYG",
    "Browns": "CLE",
    "Colts": "IND",
    "Eagles": "PHI",
    "Jaguars": "JAC",
    "Chiefs": "KC",
    "Steelers": "PIT",
    "Buccaneers": "TB",
    "Dolphins": "MIA",
    "Rams": "STL",
    "Broncos": "DEN",
    "Bengals": "CIN",
    "Cowboys": "DAL",
    "Falcons": "ATL",
    "Titans": "TEN",
    "Chargers": "SD",
    "Cardinals": "ARI",
    "Saints": "NO",
    "Texans": "HOU",
    "Vikings": "MIN",
    "49ers": "SF",
    "Ravens": "BAL",
    "Bears": "CHI",
    "Panthers": "CAR",
    "Seahawks": "SEA",
    "Raiders": "OAK",
    "Lions": "DET",
    "Patriots": "NE",
    "Packers": "GB",
}

def normalize_and_find(name):
    abbr = TEAM_MAP[name]
    return Session.query(Team).filter(Team.abbr==abbr).one()    

def scrape_spreads():
    # Returns a dict of home, away, spread
    current_season = g.serverconfig.get_value('current_season')
    current_week = api.nfl.season.current_week(season=current_season)

    games = api.nfl.game.list(season=current_season, week=current_week, no_spread=True)

    if not games:
        log.info("No games need their spreads")
        return

    log.info("{0} games need their spreads updated".format(len(games)))

    games_data = {}

    try:
        raw_data = urllib2.urlopen("http://www.cbssports.com/nfl/odds").read()
    except socket.timeout:
        log.error("Socket timeout when trying to scrape cbs site. Exiting")
        return

    soup_data = BeautifulSoup(raw_data)

    tables = soup_data.find_all("table", class_="data")

    data = []

    for table in tables:
        trs = table.find("tbody").find_all("tr")
        game_data = {}

        for i, team_row in enumerate(trs):
            if i == 0:
                for j, td in enumerate(team_row.find_all("td")):
                    if j == 1:
                        game_data['away'] = normalize_and_find(td.string)
            elif i == 1:
                for j, td in enumerate(team_row.find_all("td")):
                    if j == 1:
                        game_data['home'] = normalize_and_find(td.string)
                    elif j == 2:
                        spread = td.string
                        if spread == 'PK':
                            game_data['spread'] = 0.0
                        else:
                            game_data['spread'] = float(spread)

        data.append(game_data)

    log.info("data: {0}, {1}".format(data, len(data)))

    counter = 0

    for game in games:

        info = None
        for gd in data:

            if game.home_team_id == gd['home'].id:
                info = gd
                break

        if info is None:
            log.info("No spread found for game {0}".format(game.short_display()))
            continue

        if game.away_team_id != info['away'].id:
            log.warn(
                "Spread found for home team of game {0}, but incorrect away team".format(
                    game.short_display(),
                    info
                )
            )
            continue

        log.info("Found spread for {0} updating with spread {1}".format(game.short_display(), info['spread']))
        game.spread = info['spread']
        Session.add(game)
        counter += 1            

    Session.commit()
    log.info("Updated {0} games with their spreads".format(counter))

if __name__ == '__main__':
    import fadeben.lib.bootstrap
    scrape_spreads()
