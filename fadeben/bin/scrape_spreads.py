"""
If there's games going on right now, lets try and see if they're over by grabbing the scores from NFL's site
"""
import sys
import datetime
import logging
import os
import urllib2
import pytz

from bs4 import BeautifulSoup

from fadeben.lib.script import bootstrap
from fadeben import api
from fadeben.lib import dt

from fadeben.model import Session, Team

from pylons import app_globals as g

log = logging.getLogger("fadeben.spread_scraper")
TEAM_MAP = {
    "Buffalo": "BUF",
    "Washington": "WAS",
    "N.Y. Jets": "NYJ",
    "N.Y. Giants": "NYG",
    "Cleveland": "CLE",
    "Indianapolis": "IND",
    "Philadelphia": "PHI",
    "Jacksonville": "JAC",
    "Kansas City": "KC",
    "Pittsburgh": "PIT",
    "Tampa Bay": "TB",
    "Miami": "MIA",
    "St. Louis": "STL",
    "Denver": "DEN",
    "Cincinnati": "CIN",
    "Dallas": "DAL",
    "Atlanta": "ATL",
    "Tennessee": "TEN",
    "San Diego": "SD",
    "Arizona": "ARI",
    "New Orleans": "NO",
    "Houston": "HOU",
    "Minnesota": "MIN",
    "San Francisco": "SF",
    "Baltimore": "BAL",
    "Chicago": "CHI",
    "Carolina": "CAR",
    "Seattle": "SEA",
    "Oakland": "OAK",
    "Detroit": "DET",
    "New England": "NE",
    "Green Bay": "GB",
}

def normalize_and_find(name):

    abbr = TEAM_MAP[name]

    team = Session.query(Team).filter(Team.abbr==abbr).one()

    return team

def scrape_spreads():

    raw_data = urllib2.urlopen("http://www.covers.com/odds/football/nfl-spreads.aspx").read()

    soup_data = BeautifulSoup(raw_data)

    #log.debug("data: {0}".format(soup_data))

    # Step 3: Go through and check if we can find this game in the shitty data.
    container_div = soup_data.find("div", class_="CustomOddsContainer")
    odds_table = container_div.find("table")

    games = []
    
    for i, row in enumerate(odds_table.find_all("tr")):
        if not row.attrs.get('id', '').startswith("/sport/football/competition"):
            continue

        # We've (hopefully) got a row in the table that represents 
        # a football game.
        i += 1
        team_td = row.find("td")
        # The first td holds the team information
        away_team_information_div = team_td.find("div", class_="team_away")
        #away_team_information_div = away_team_information_td.find("div")
        away_team_str = away_team_information_div.find("strong").string

        home_team_information_div = team_td.find("div", class_="team_home")
        home_team_str = home_team_information_div.find("strong").string

        if home_team_str.startswith("@"):
            home_team_str = home_team_str[1:]


        # Try and find the game time for this game to make sure
        # we're in the same ballpark
        time_td = team_td.next_sibling.next_sibling # fucking whitespace

        time_str = time_td.find("div", class_="team_away").string.strip()
        # parse the string
        time = datetime.datetime.strptime(time_str, "%a, %b %d")

        print "time = {0}".format(time)
        

        # The open spreads are in the first "offshore_top" td
        spread_td = row.find("td", class_="offshore_top")
        # The spread is in the "offshore" div
        spread = spread_td.find("div", class_="offshore").string.strip()

        # Normalize a 'pickem'
        if spread == "pk":
            spread = 0

        # Now we need to normalize the team names to something we can actually use
        home_team = normalize_and_find(home_team_str)
        away_team = normalize_and_find(away_team_str)

        games.append(
            {"home_team": home_team,
             "away_team": away_team,
             "spread": float(spread),
             "gametime": time,
         }
        )

        print "{0} at {1} with {2}".format(away_team_str, home_team_str, spread)

    return games

def run_it():
    log.info("Automatic spread scraper starting...")
    # Step one: find any games in the current week
    # that don't have their spreads set
    current_season = g.serverconfig.get_value('current_season')
    
    current_week = api.nfl.season.current_week(season=current_season)

    games = api.nfl.game.list(season=current_season, week=current_week, no_spread=True)

    # Step two: if said games exist, get the scores from the NFL site

    if not games and False:
        log.info("No games need their spreads")
        return

    log.info("{0} games in progress.  Checking for scores".format(len(games)))
    
    # We've got games to check for, let's go parse the covers site
    game_map = scrape_spreads()

    log.info("Got game map back from parsed covers site: {0}".format(game_map))
    
    # Now we go through our games that need spreads and check if we've got
    # something for them.
    counter = 0
    for game in games:
        # Look for the game in the map
        sm = None
        for spread_map in game_map:
            if game.home_team_id == spread_map['home_team'].id:
                sm = spread_map
                break

        if sm is None:
            log.info("No spread in the map for game {0}".format(game.short_display()))
            continue

        # Looks like we've got a spread! Let's do some basic validation to
        # make sure we're not going to fuck up everything
        if game.away_team_id != sm['away_team'].id:
            log.warn("Spread found for game {0} with matching home team, but mismatched away team! Spread data: {1}".format(
                game.short_display(), sm
            )
            )
            continue
        
        
        if game.game_time_l.month != sm['gametime'].month \
           or game.game_time_l.day != sm['gametime'].day:
            # something's whack yo.
            log.warn("Spread found for {0} with the right teams, but the date appears wrong.  Skipping. on file {1}, {2}".format(
                game.short_display(), game.game_time, sm
            )
            )
            continue

        log.info("Found spread for {0}.  Updating record with data: {1}".format(game.short_display(), sm) )

        game.spread = sm['spread']
        Session.add(game)
        counter += 1

    Session.commit()
    log.info("Updated {0} games with their spreads".format(counter))

    # step 5: profit!
    log.info("Done scraping for spreads")

def main():
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = 'development.ini'

    proj_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    bootstrap(config_file, proj_dir)
    run_it()

if __name__ == '__main__':
    main()

