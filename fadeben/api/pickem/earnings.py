import logging
import datetime

from unstdlib.standard import get_many

from fadeben.model import Session, Member, User, Season

from fadeben.api.pickem import prediction, member, season as pickem_season_api

log = logging.getLogger(__name__)

def calculate(**params):
    """
    Calculate the weekly winners.  

    This does *not* calculate the overall season pick winner.

    :param season
    """
    # Step 1 - get get all the completed picks in the season
    season_num = params['season']
    members = member.list(season=season_num)
    pick_map = prediction.count_user_week(season_id=season_num, user_ids=[m.id for m in members])

    weeks_completed = pickem_season_api.weeks_completed_p(season_id=season_num)

    log.debug("weeks completed: {0}".format(weeks_completed))

    # Step 2 - walk backwards, tagging winners in an array
    earning_map = [None] * (weeks_completed + 1)
    for i in xrange(weeks_completed, 0, -1):
        winner = [members[0].id ]
        for m in members[1:]:
            if pick_map[m.id].get(i, 0) > pick_map[winner[0]].get(i, 0):
                winner = [m.id]
            elif pick_map[m.id].get(i, 0) == pick_map[winner[0]].get(i, 0):
                winner.append(m.id)

        if len(winner) > 1:
            # There was a tie this week.  See if we can settle it form weeks after this one.
            r = _look_ahead(pick_map, i, winner, weeks_completed) 
            if r is False:
                earning_map[i] = winner
            else:
                earning_map[i] = r
        else:
            earning_map[i] = winner[0]

    return earning_map

def overall_winner(**params):
    """
    Find the season overall winner.

    Returns None if the season isn't over
    :param season_id
    """
    season_id = params['season_id']
    
    # check to see if the season is over.

    is_over = pickem_season_api.is_over(season_id=season_id)

    if not is_over:
        log.debug("Season {0} not over.  Returning no winner.".format(season_id))
        return None

    members = member.list(season=season_id)

    # Get the pick map
    m = prediction.count_user_picks_raw(season=season_id, user_ids=[x.id for x in members])

    winner = None

    for banana, c in m.items():
        if winner is None:
            winner = banana
            continue

        if c > m[winner]:
            winner = banana

    return winner

def _look_ahead(pick_map, week, winners, total_weeks):
    """
    Week x was a tie, so look ahead at future weeks to see
    if we can settle the tie
    """
    w = list(winners) # make a local copy to manipulate
    
    if week > total_weeks:
        return False

    top = [ w[0] ]
    for member_id in w[1:]:
        if pick_map[member_id][week] > pick_map[top[0]][week]:
            top = [ member_id ]
        elif pick_map[member_id][week] == pick_map[top[0]][week]:
            top.append(member_id)

    if len(top) > 1:
        return _look_ahead(pick_map, week+1, top, total_weeks)
    else:
        return top[0]
