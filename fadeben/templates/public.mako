# -*- coding: utf-8 -*-
<!DOCTYPE html>
<html lang="en">
<head>
    <title>The FadeBen project</title>
    ${ h.stylesheet_link('/css/desktop.css') }
    <script type="text/javascript">var FadeBen = FadeBen || {};</script>
    ${ h.javascript_link('/js/jquery-1.7.2.min.js') }
    ${ h.javascript_link('/js/underscore.js') }
    ${ h.javascript_link('/js/backbone.js') }
    ${ h.javascript_link('/js/fadeben.js') }
</head>
<body>
<div id="page">
    <div id="header">
       <h1 id="logo">${ h.link_to("FadeBen", url("homepage")) }</h1>
       <ul id="navigation">
           <li>${ h.link_to("home", url("homepage")) }</li>
           <li>${ h.link_to("standings", url("standings", season=h.g.current_season)) }</li>
           <li>${ h.link_to("predictions", url("prediction_season", season_id=h.g.current_season)) }</li>
           <li>${ h.link_to("account", url("settings") ) }</li>
       </ul>
    </div>
    <div id="content_wrapper">
	<% messages = h.flash.pop_messages() %>
	% if messages:
	<ul id="flash-messages">
	    % for message in messages:
	    <li class="msg ${ message.category }">${ message }</li>
	    % endfor
	</ul>
	% endif
        ${ next.body() }
    </div>
    <div id="footer">
	% if hasattr(c, 'user'):
        <ul class="right">
            <li>${ h.link_to("teams", url("teams") ) }</li>
            <li>${ h.link_to("schedule", url("season_schedule", season=h.g.current_season) ) }</li>
	    % if h.serverconfig.is_enabled('earnings_calculator'):
            <li>${ h.link_to("earnings", url("earnings", season_id=h.g.current_season) ) }</a></li>
	    % endif
            <li>${ h.link_to("logout", url("logout")) }</li>
        </ul>
	% endif
    </div>
</div>
<!-- <div id="overlay-container"> -->
<!--     <div class="content">Hello world</div> -->
<!-- </div> -->
% if false:
<script type="text/javascript" src="/js/models.js"></script>
% endif
</body>

</html>
