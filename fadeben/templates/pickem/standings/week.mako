# -*- coding: utf-8 -*-
<%inherit file="/public.mako"/>
<div class="main-content">
    <%
         chunks = [c.games[:8], c.games[8:]]
    %>
    <div class="left sidebar">
        <h3>Week ${ c.week }</h3>
        <ul>
            % for m in c.week_standings:
            <li>${ m.first_name }: ${ c.pick_map.get(m.id, 0) }</li>
            % endfor
        </ul>
        <h3>Overall</h3>
        <ul>
            % for m in c.overall_standings:
            <li>${ m.first_name }: ${ c.season_map.get(m.id, 0) }</li>
            % endfor
        </ul>    
    </div>

    <div class="sidebar-pad">
        <div class="sub-header" style="overflow: hidden;">
            <h1 class="left">Standings - Week ${ c.week }</h1>
            % if not c.week_completed:
                ${ h.link_to("Make predictions", url("prediction_season_week", season_id=c.season_num, week=c.week), class_="button right", id="make-predictions")}
            % else:
                <span class="right completed">completed</span>
            % endif
        </div>
        % for chunk in chunks:

        % if not chunk:
            <% continue %>
        % endif

        <div class="data-table week-standings-table">
            <div>
                <div class="cell header"></div>
                % for game in chunk:
                <div class="cell header">
                    <a href="#" class="sub-menu-launcher">${ game.away_team.abbr }<span style="font-size: 8px;"> @ </span>${ game.home_team.abbr }
                        <span style="font-size: 10px;">(${ h.show_spread(game.spread) })</span>
                    </a>
                    <div class="drop-down-menu">
                        <h3>${ game.away_team.name } at ${ game.home_team.name }</h3>
                        <p>${ game.game_time_l }</p>
                    </div>
                </div>
                % endfor
            </div>
            % for member in c.members:
            <div>
                <div class="cell">${ member.first_name }</div>
                % for game in chunk:
                ${ show_prediction(c.user, game, c.map.get(member.id, {}).get(game.id)) }
                % endfor
            </div>
            % endfor
        </div>

        % endfor
    </div>
</div>

% if c.interactive_picks:
${ h.javascript_link('/js/bootstrap/pickem/standings/week.js') }
% else:
${ h.javascript_link('/js/bootstrap/pickem/standings/season.js') }
% endif
<%def name="show_prediction(user, game, prediction)">
<div class="cell ${ h.prediction_result_class(user, game, prediction) }">
    ${ h.show_prediction(user, game, prediction) }
</div>
</%def>
