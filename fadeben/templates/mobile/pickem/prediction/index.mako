# -*- coding: utf-8 -*-
<%inherit file="/mobile/public.mako"/>

% if c.games:

% for game in c.games:
${ h.form(url('bulk_save_predictions', next=url('week_standings', season=c.season, week=c.week) ), method="put") }
<% pred = c.pmap.get(game.id) %>
<h3>${ game.short_display() } (${ h.show_spread(game.spread) })</h3>
${ h.hidden("game", game.id) }
<fieldset data-role="controlgroup">
    ${ h.radio("prediction-{0}".format(game.id), False, id="game-{0}-away".format(game.id), checked=(pred is False)) }
    <label for="game-${ game.id }-away">${ game.away_team.name }</label>
    ${ h.radio("prediction-{0}".format(game.id), True, id="game-{0}-home".format(game.id), checked=(pred is True)) }
    <label for="game-${ game.id }-home">${ game.home_team.name }</label>
</fieldset>
% endfor

<button type="submit" data-theme="a">Submit</button>
${ h.end_form() }


% else:
<p>There are no more games left to predict this week.</p>
<p>You can go ${ h.link_to('check out the standings', url('week_standings', season=c.season, week=c.week)) } to see the results</p>
% endif

<%def name="header_text()">
Predictions
</%def>
