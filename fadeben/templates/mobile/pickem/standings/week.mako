# -*- coding: utf-8 -*-
<%inherit file="/mobile/public.mako"/>

<table id="week-standings-count">
    <tr>
        % for member in c.members:
        <th>${ member.first_name }</th>
        % endfor
    </tr>
    <tr>
        % for member in c.members:
        <td>${ c.season_map.get(member.id, 0) }</td>
        % endfor
    </tr>
</table>

% for game in c.games:
    <h3>${ game.short_display() } (${ h.show_spread(game.spread) })</h3>

    <% choices = list('abc') %>
    <div class="ui-grid-b">
        % for i, member in enumerate(c.members):
        <div class="prediction ui-block-${ h.cycle(i, choices) } ${ h.prediction_result_class(c.user, game, c.map.get(member.id, {}).get(game.id)) }">
            <span class="name">${ member.first_name }</span>
            ${ h.show_prediction(c.user, game, c.map.get(member.id, {}).get(game.id)) }
        </div>
        % endfor
    </div>
% endfor

<%def name="header_text()">
<a href="${ url('week_standings', season=c.season_num, week=c.week-1) }" data-role="button" data-icon="arrow-l" data-iconpos="notext" data-direction="reverse">prev</a>
Week ${ c.week } standings
<a href="${ url('week_standings', season=c.season_num, week=c.week+1) }" data-role="button" data-icon="arrow-r" data-iconpos="notext">next</a>
</%def>

<%def name="show_prediction(user, game, prediction)">
</%def>
