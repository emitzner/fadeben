# -*- coding: utf-8 -*-
<%inherit file="/public.mako"/>

<div class="main-content">
    <h1>Predictions for week ${ c.week }</h1>

	% if c.games:
    ${ h.form(url("bulk_save_predictions", next=url("week_standings", season=c.season, week=c.week)), method="put") }
    % for game in c.games:
    <%include file="/shared/prediction.mako" args="game=game,pred=c.pmap.get(game.id)"/>
    ${ h.hidden("game", game.id) }
    % endfor

    ${ h.submit("update", "Save") }
    ${ h.end_form() }
	% else:
	<h2>There's no more games left to predict</h2>
	<p>All the games have already started.  
		Go ${ h.link_to("check out the standings page", url("week_standings", season=c.season, week=c.week)) }
		to see the results.
		</p>
	% endif
    
</div>
