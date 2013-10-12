# -*- coding: utf-8 -*-
<%inherit file="/bootstrap/public.mako"/>

<div class="panel panel-default">
  <!-- Default panel contents -->
  <div class="panel-heading">NFC East</div>

  <!-- List group -->
  <div class="list-group">
      % for team in c.teams:
      <a href="${ url('show_team', abbr=team.abbr) }" class="list-group-item">${ team.name }</a>
      % endfor
  </div>
</div>
