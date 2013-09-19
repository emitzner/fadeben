import logging

from pylons import request, response, session, tmpl_context as c, url, app_globals as g
from pylons.controllers.util import abort, redirect

from fadeben.lib.base import BaseController, render
from fadeben import api

from fadeben.model import Session, User

log = logging.getLogger(__name__)

class StandingsController(BaseController):

    def season(self, season):
        c.season = api.nfl.season.find(season=season)
        c.weeks = c.season.num_weeks
        log.debug("NUM WEEKS: {0}".format(c.weeks))
        c.members = api.pickem.member.list(season=season)

        grouped_playoff_enabled = g.serverconfig.is_enabled('grouped_playoff')
        
        if grouped_playoff_enabled:
            c.weeks_completed = api.pickem.season.weeks_completed_p(season_id=season)
            # Adding 1 to num_weeks accounts for the grouped playoff week for pickem.
            c.min_weeks_to_show = min(c.weeks_completed + 3, c.season.num_weeks+1)
        else:
            c.weeks_completed = api.nfl.season.weeks_completed(season=season)
            c.min_weeks_to_show = min(c.weeks_completed + 3, c.season.num_total_weeks)

        log.debug("Weeks completed: {0}".format(c.weeks_completed))

        # Calculate weekly groupings.
        # todo - this is display logic, and as such shouldn't live in the controller.
        group_amount = 3
        num_groups = (max(c.weeks_completed-2, 0)) / group_amount

        c.groups = []
        c.group_end = 0
        for group in xrange(num_groups):
            start = group * group_amount
            end = start + group_amount
            c.groups.append( {'start': start, 'end': end } )
            c.group_end = end

        log.debug("num_groups: {0}".format(num_groups))
        log.debug("group end: {0}".format(c.group_end))

        # Get the correct number of predictions for each user
        # this season.
        member_ids = [x.id for x in c.members]
        c.season_map = api.pickem.prediction.count_user_picks_raw(
            season=season,
            user_ids=member_ids,
            )

        # Get the number of correct picks by user by week.
        if grouped_playoff_enabled:

            c.week_map = api.pickem.prediction.count_user_week(
                season_id=season,
                user_ids=member_ids
                )
        else:
            c.week_map = api.pickem.prediction.count_user_week_raw(
                season=season,
                user_ids=member_ids
                )

        log.debug("season map: {0}".format(c.season_map))
        log.debug("week map: {0}".format(c.week_map))

        # Sort the members by their overall count
        c.members = sorted(c.members,
                           key=lambda x: c.season_map.get(x.id, 0),
                           reverse=True)

        return render('/pickem/standings/season.mako')

    def week(self, season, week):
        """Display the standings for a particular week"""

        # HACK: Fix before enabling
        grouped_playoff_enabled = g.serverconfig.is_enabled('grouped_playoff')

        if grouped_playoff_enabled and int(week) > 17:
            log.debug("yo banana {0}".format(week))
            c.games = api.nfl.game.list(season=season, playoffs=True)
        else:
            log.debug("Not grouping playoff games")
            c.games = api.nfl.game.list(season=season, week=week)

        c.members = api.pickem.member.list(season=season)
        c.week = int(week)
        c.season_num = season

        c.week_completed = True

        c.interactive_picks = g.serverconfig.is_enabled('interactive_picks')
        # is the week completed?
        for game in c.games:
            if not game.finished():
                c.week_completed = False
                break
            log.debug("game {0} is finished, {1}".format(game.id, game.home_score == ''))

        c.map = api.pickem.prediction.list_by_user(
            season=season,
            user_ids=[x.id for x in c.members],
            game_ids=[x.id for x in c.games],
            )

        c.season_map = api.pickem.prediction.count_user_picks_raw(
            season=season,
            user_ids=[x.id for x in c.members],
            )

        log.debug("season map count: {0}".format(c.season_map))

        c.pick_map = api.pickem.prediction.count_user_picks_raw(
            season=season,
            user_ids=[x.id for x in c.members],
            week=c.week)

        c.week_standings = sorted(c.members,
                                  key=lambda x: c.pick_map.get(x.id, 0),
                                  reverse=True)

        c.overall_standings = sorted(c.members,
                                  key=lambda x: c.season_map.get(x.id, 0),
                                  reverse=True)


        log.debug("pick map: {0}".format(c.pick_map))

        log.debug("map: {0}".format(c.map))
        
        return render('/pickem/standings/week.mako')
