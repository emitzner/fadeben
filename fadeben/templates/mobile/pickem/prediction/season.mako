# -*- coding: utf-8 -*-
<%inherit file="/mobile/public.mako"/>

% if c.current_week:
<ul data-role="listview">
    % for i in xrange(c.current_week, c.season.num_total_weeks+1):
    <li>
        <a href="${ url('prediction_season_week', season_id=c.season.number, week=i) }" data-ajax="false">
            ${ h.week_name(c.season, i) }
            % if i == c.current_week:
            (current)
            % endif
        </a>
    </li>
    % endfor
</ul>
% else:
<p>There's no more games left to predict this season.</p>
% endif


<%def name="header_text()">
</%def>
