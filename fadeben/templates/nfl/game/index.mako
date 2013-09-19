# -*- coding: utf-8 -*-
<%inherit file="/public.mako"/>

zomg it's all the games!

<ul>
    % for game in c.games:
    <li>${ h.link_to(game.away_team.name, url('show_team', abbr=game.away_team.abbr)) }
        @
        ${ game.home_team.name }</li>
    % endfor
</ul>
