# -*- coding: utf-8 -*-
<%inherit file="/mobile/public.mako"/>

<h3>Overall</h3>
<table class="spaced-table">
    <tr>
        % for member in c.members:
        <td>${ member.first_name }</td>
        % endfor
    </tr>
    <tr>
        % for member in c.members:
        <td>${ c.season_map.get(member.id, 0) }</td>
        % endfor
    </tr>
</table>

% for week in xrange(c.min_weeks_to_show, 0, -1):
<h3>
    % if h.g.serverconfig.is_enabled('grouped_playoff') and c.season.is_playoff_week(week):
    <a href="${ url('playoff_standings', season=c.season.number) }">
        Playoffs
    </a>
    % else:
    <a href="${ url('week_standings', season=c.season.number, week=week) }">
        Week ${ week }
    </a>
    % endif
</h3>
<table class="spaced-table">
    <tr>
        % for member in c.members:
        <td>${ member.first_name }</td>
        % endfor
    </tr>
    <tr>
        % for member in c.members:
        <td>${ c.week_map.get(member.id, {}).get(week, 0) }</td>
        % endfor
    </tr>
</table>
% endfor

<%def name="header_text()">
Season standings
</%def>
