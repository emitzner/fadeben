# -*- coding: utf-8 -*-
<%inherit file="/public.mako"/>

<div class="main-content">
    <h1>Standings - Season ${ c.season.number }</h1>
    
    <div class="table">
	<div class="header">
	    <div>Name</div>
            % for group in c.groups:
            <div class="drop-down-container">
		${ h.link_to("Weeks {0} - {1}".format(group['start'] + 1, group['end']),
		"#", 
		class_="sub-menu-launcher") }
		<div class="drop-down-menu">
		    <ul>
			% for i in xrange(group['start'] + 1, group['end']+1):
			<li>
			    ${ h.link_to(h.week_name(c.season, i),
                            url("week_standings", season=c.season.number, week=i))
			    }
			</li>
			% endfor
		    </ul>
		</div>
	    </div>
	    % endfor

	    % for week in xrange(c.group_end+1, c.min_weeks_to_show+1):
	    <div>
                % if h.g.serverconfig.is_enabled('grouped_playoff') and c.season.is_playoff_week(week):
		${ h.link_to("Playoffs",
                    url("playoff_standings", season=c.season.number)
                )
		}
                    
                % else:
		${ h.link_to(h.week_name(c.season, week),
		    url("week_standings", season=c.season.number, week=week)) 
		}
                % endif
	    </div>
	    % endfor
	    <div>Total</div>
	</div>
	## peeps
	% for member in c.members:
	<div>
	    <div>${ member.first_name }</div>

		## Grouped weeks
	    % for group in c.groups:
	    <div>
			${ h.get_grouped_picks(
			c.week_map, c.season, member, group['start'], group['end']) }
	    </div>
	    % endfor

		## Individual weeks
	    % for week in xrange(c.group_end+1, c.min_weeks_to_show+1):
	    <div>
			${ h.get_num_picks_for_week(c.week_map, c.season, member, week) }
	    </div>
	    % endfor
	    <div>${ c.season_map.get(member.id, 0) }</div>
	</div>
	% endfor
    </div>
</div>

${ h.javascript_link('/js/bootstrap/pickem/standings/season.js') }
