# -*- coding: utf-8 -*-
<%inherit file="/public.mako"/>

<div class="main-content">
    <h1>Schedule - ${ c.team.name }</h1>
    <h2>Record: ${ h.show_record(c.record) }</h2>
    <h2>Record ATS: ${ h.show_record(c.record_ats) }</h2>

    <table class="data">
        <tr>
            <th class="blank"></th>
            <th>Time</th>
            <th>Away</th>
            <th>Home</th>
            <th>Result</th>
            <th>
                <acronym title="Against the Spread">ATS</acronym>
            </th>
        </tr>
        % for pos, game in enumerate(c.games):

        % if game is None:
        ## BYE WEEK
            <tr class="${ h.row_color(pos+1) }">
		<td>${ self.week_link(pos+1) }</td>
		<td colspan="5">Bye Week</td>
            </tr>
        % else:
            <tr class="${ h.row_color(game.week) }">
		<td>${ self.week_link(game.week) }</td>
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
		<td class="${ h.game_result_class(c.team, game) }">
                    % if game.home_score is not None:
                    ${ game.away_score } - ${ game.home_score }
                    % else:
                    -
                    % endif
		</td>
		<td class="${ h.game_result_class(c.team, game, True) }">
                    ${ h.show_spread(game.spread) }
		</td>
            </tr>
        % endif

        % endfor
    </table>
</div>

<%def name="week_link(i)">
${ h.link_to("Week {0}".format(i),
url("week_schedule", season=c.current_season.number, week=i) ) }
</%def>
