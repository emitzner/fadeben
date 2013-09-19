# -*- coding: utf-8 -*-
<%inherit file="/public.mako"/>

<div class="main-content">

    ${ h.form(url("save_games", next=request.path), method="post") }
    <div class="table">
	<div class="header">
	    <div>Game</div>
	    <div>Spread</div>
	    <div>Away Score</div>
	    <div>Home Score</div>
	</div>
        
	% for game in c.games:
	<div>
	    <div>${ game.away_team.abbr } @ ${ game.home_team.abbr }</div>
	    <div>${ h.text("game-{0}-spread".format(game.id), game.spread, autocomplete="off") }</div>
	    <div>${ h.text("game-{0}-away-score".format(game.id), game.away_score, autocomplete="off") }</div>
	    <div>${ h.text("game-{0}-home-score".format(game.id), game.home_score, autocomplete="off") }</div>
	    ${ h.hidden("games", game.id) }
	</div>
	% endfor
    </div>
    ${ h.submit("save", "Update games") }
    ${ h.end_form() }
</div>
