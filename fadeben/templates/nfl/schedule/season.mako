# -*- coding: utf-8 -*-
<%inherit file="/public.mako"/>

<div class="main-content">

<h1>Season ${ c.season.number }</h1>

<ul>
    % for week in xrange(1, c.season.num_total_weeks+1):
    <li>${ h.link_to(h.week_name(c.season, week), url('week_schedule',
        season=c.season.number, week=week)) }</li>
    % endfor
</ul>
</div>
