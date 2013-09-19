import logging

from fadeben.api.nfl import season as season_api

log = logging.getLogger(__name__)

__all__ = ['weeks_completed_p', 'is_over']

def weeks_completed_p(**params):
    """Returns the number of weeks that were completed in a given season.

    This function counts all playoff weeks as one continuous week.
    """

    season_id = params['season_id']
    season = season_api.find(season=season_id)

    # Get the current week unaltered.
    weeks_completed_raw = season_api.weeks_completed(season=season_id)

    if weeks_completed_raw <= season.num_weeks:
        # We're not into the playoffs.
        return weeks_completed_raw

    # We're into playoffs.
    if weeks_completed_raw == season.num_total_weeks:
        return season.num_weeks + 1
    else:
        return season.num_weeks

def is_over(**params):
    # hack: this doesn't work if we ever go to a different
    # number of weeks per season, but whatever
    season_id = params['season_id']
    weeks_completed = weeks_completed_p(season_id=season_id)

    return (weeks_completed == 18)
