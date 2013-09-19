# -*- coding: utf-8 -*-
<%inherit file="/public.mako"/>

<div class="main-content">
<h1>Season ${ c.season.number }</h1>

<ul>
	% for i in xrange(1, c.season.num_total_weeks+1):
	<li>
		${ h.link_to(h.week_name(c.season, i), url("prediction_season_week", season_id=c.season.number, week=i) ) }
	</li>
	% endfor
</div>
