# -*- coding: utf-8 -*-
<%inherit file="/mobile/public.mako"/>

<ul data-role="listview">
    % for week in xrange(1, c.season.num_weeks+1):

    <li>
        <a href="${ url('week_schedule', season=c.season.number, week=week) }">
            Week ${ week }
        </a>
    </li>
    % endfor
</ul>

<%def name="header_text()">
Season Schedule
</%def>
