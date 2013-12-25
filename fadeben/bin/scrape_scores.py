"""
If there's games going on right now, lets try and see if they're over by grabbing the scores from NFL's site
"""
import sys
import logging
import os
import urllib2
import simplejson as json

from fadeben.lib.script import bootstrap
from fadeben import api

from pylons import app_globals as g

log = logging.getLogger("fadeben.scores")

def parse_scores():
    log.info("Automatic score scraper starting...")
    # Step one: find any games that have started but have no score.
    current_season = g.serverconfig.get_value('current_season')

    games = api.nfl.game.list(season=current_season, in_progress=True)

    # Step two: if said games exist, get the scores from the NFL site

    if not games:
        log.info("No games in progress")
        return

    log.info("{0} games in progress.  Checking for scores".format(len(games)))

    raw_data = urllib2.urlopen("http://www.nfl.com/liveupdate/scores/scores.json").read()

    data = json.loads(raw_data)

    # Step 3: go through each game and see if the game is over on the nfl site.
    for game in games:
        # find this game in the
        for k in data:
            if data[k]['home']['abbr'] == game.home_team.abbr \
                    and data[k]['away']['abbr'] == game.away_team.abbr:
                # check to see if game is over:
                result = data[k]['qtr'].lower()

                if 'final' in result:
                    # update the game
                    h_s = data[k]['home']['score']['T']
                    a_s = data[k]['away']['score']['T']
                    log.info("Updating game {0} with {1} / {2}".format(game.short_display(), a_s, h_s))
                    api.nfl.game.update(game_id=game.id, home_score=h_s, away_score=a_s)
                continue

    # step 5: profit!
    log.info("Done scraping for scores.")

if __name__ == '__main__':
    import fadeben.lib.bootstrap
    parse_scores()

