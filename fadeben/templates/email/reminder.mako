Hi ${ c.user.first_name },

There's ${ len(c.games) } games you haven't predicted yet, that are going to start today.

The games:
% for game in c.games:
${ game.short_display() }, (${ h.show_spread(game.spread) })
% endfor

To make your predictions, go here:
${ url("prediction_season_week", season_id=c.season, week=c.week, qualified=True) }

Enjoy.

