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
