# -*- coding: utf-8 -*-
<%inherit file="/mobile/public.mako"/>

<ul data-role="listview" data-filter="true">
    % for team in c.teams:
    <li><a href="${ url('show_team', abbr=team.abbr) }" data-ajax="false" />${ team.name }</a></li>
    % endfor
</ul>


<%def name="header_text()">
Teams
</%def>
