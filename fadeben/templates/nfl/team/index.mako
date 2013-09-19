# -*- coding: utf-8 -*-
<%inherit file="/public.mako"/>

<div class="main-content">
	<h1>Teams</h1>

	<ul>
		% for team in c.teams:
		<li>${ h.link_to(team.name, url("show_team", abbr=team.abbr) ) }</li>
		% endfor
	</ul>
</div>
