# -*- coding: utf-8 -*-
<%inherit file="/bootstrap/public.mako"/>

<div class="page-header">
    <h1>${ c.team.name } <small>Schedule</small></h1>
</div>

<div class="table-responsive">
    <table class="table table-striped">
        <tr>
            <th></th>
            <th>Time</th>
	    <th>Away</th>
	    <th>Home</th>
	    <th>Result</th>
	    <th>
	        <acronym title="Against the Spread">ATS</acronym>
	    </th>

        </tr>
        <% last_week = 0; i = 0; %>

        % for game in c.games:
        % if game.week != last_week+1:
        <tr>
            <td>${ self.week_link(i) }</td>
            <td colspan="5">Bye week</td>
        </tr>
        <% i += 1 %>
        % endif
        <tr>
            <td>${ self.week_link(i) }</td>
            <td>${ game.game_time_l.strftime("%a %m/%d %I:%M") }</td>
            <td>
	        ${ h.link_to_if(
	        c.team.id != game.away_team_id,
	        game.away_team.name, url("show_team", abbr=game.away_team.abbr)) 
	        }
	    </td>
	    <td>
	        ${ h.link_to_if(
	        c.team.id != game.home_team_id,
	        game.home_team.name, url("show_team", abbr=game.home_team.abbr))
	        }
	    </td>
	    <td class="${ self.score_result_class(game, c.team, False) }" >
	        % if game.home_score is not None:
	        ${ game.away_score } - ${ game.home_score }
	        % else:
	        -
	        % endif
	    </td>
	    <td class="${ self.score_result_class(game, c.team, True) }">
	        ${ h.show_spread(game.spread) }
	    </td>
        </tr>
        <% last_week = game.week; i += 1 %>

        % endfor

    </table>
</div>
<%def name="week_link(i)">
${ h.link_to("Week {0}".format(i+1),
url("week_schedule", season=c.current_season.number, week=i+1) ) }
</%def>

<%def name="score_result_class(game, team, ats)" filter="h, trim">
% if game.is_completed():

% if game.is_winner(team, ats):
success
% elif game.home_score == game.away_score:
active
% else:
danger
% endif

% endif
</%def>
