<!DOCTYPE html> 
<html> 
    <head> 
        <title>The FadeBen Project</title> 
        <meta name="viewport" content="width=device-width, initial-scale=1"> 
        <link rel="stylesheet" href="http://code.jquery.com/mobile/1.1.1/jquery.mobile-1.1.1.min.css" />
        <link rel="stylesheet" href="/css/mobile.css" />
        <script src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
        <script src="http://code.jquery.com/mobile/1.1.1/jquery.mobile-1.1.1.min.js"></script>
	<meta http-equiv="Content-language" content="en" />
	<!-- <meta charset="UTF-8" /> -->
	<!-- <meta name="google" content="notranslate"> -->
</head> 
<body>

    <div data-role="page">

        <div id="header" data-role="header">
            <!-- <h1>${ self.header_text() }</h1> -->
            <div data-role="navbar" data-iconpos="left">
                <ul>
                    <li><a href="${ url('standings', season=h.g.current_season) }" data-icon="grid">Standings</a></li>
                    <li><a href="${ url('prediction_season', season_id=h.g.current_season) }" data-icon="check">Predictions</a></li>
                    <li><a href="${ url('settings') }" data-icon="gear">Account</a></li>
                </ul>
            </div>
        </div><!-- /header -->
        
        <div data-role="content">
	    <% messages = h.flash.pop_messages() %>
	    % if messages:
	    <ul id="flash-messages">
	        % for message in messages:
	        <li class="msg ${ message.category }">${ message }</li>
	        % endfor
	    </ul>
	    % endif

            ${ self.body() }
        </div><!-- /content -->

% if false:
## TODO: when the rest of the site is transferred to mobile, this can 
## be reactivated.        
        <div data-role="footer">
            <div data-role="navbar">
                <ul>
                    <li><a href="${ url('teams') }">Teams</a></li>
                    <!-- <li><a href="${ url('season_schedule', season=h.g.current_season) }">Schedule</a></li> -->
                    <li><a href="${ url('settings') }">Account</a></li>
                </ul>
            </div>
        </div>
% endif
    </div><!-- /page -->

</body>
</html>


<%def name="header_text()">
FadeBen
</%def>
