# -*- coding: utf-8 -*-
<%inherit file="/public.mako"/>

<div class="main-content">
    <h1>Week ${ c.week }</h1>
	
	<table class="data">
		<tr>
			<th>Time</th>
			<th>Away</th>
			<th>Home</th>
			<th>Spread</th>
			<th>Result</th>
		</tr>
		% for i, game in enumerate(c.games):
		<tr class="${ h.row_color(i) }">
			<td>${ game.game_time_l.strftime("%a %m/%d %I:%M") }</td>
			<td>
				${ h.link_to(game.away_team.name,
				url("show_team", abbr=game.away_team.abbr))
				}
			</td>
			<td>
				${ h.link_to(game.home_team.name,
				url("show_team", abbr=game.home_team.abbr))
				}
			</td>
			<td>${ h.show_spread(game.spread) }</td>
			<td>
				% if game.is_finished():
				${ game.away_score } ${ game.away_team.abbr } - ${ game.home_team.abbr } ${ game.home_score }
				% else:
				-
				% endif
			</td>
		</tr>
		% endfor
	</table>

	% if not c.week_completed:
    <div>${ h.link_to('Make predictions', url("prediction_season_week", season_id=h.g.current_season, week=c.week) ) }</div>
	% endif
</div>
