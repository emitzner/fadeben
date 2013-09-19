"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.connect('homepage', '/', controller='welcome', action='homepage')

    # Account routes
    map.connect('login', '/account/login', controller="account", action="login")
    map.connect('logout', '/account/logout', controller="account", action="logout")

    map.connect('settings', '/account/settings',
                controller="account", action="settings")

    map.connect('change_password', '/account/change_password',
                controller="account", action="change_password")
    map.connect('change_password_submit', '/account/change_password/submit',
                controller="account", action="change_password_submit")

    map.connect("reset_password", '/account/reset_password',
                controller="account", action="forgot_password")
    
    # NFL routes
    # NFL Teams
    map.connect('teams', '/nfl/teams',
                controller='nfl/team', action='index')
    map.connect('show_team', '/nfl/teams/{abbr}',
                controller='nfl/team', action='view')

    # NFL Season
    map.connect('seasons', '/nfl/seasons',
                controller='nfl/season', action='index')

    map.connect("show_season", '/nfl/seasons/{number}',
                controller='nfl/season', action='view',
                conditions=dict(method=["GET"]))

    # to be deleted / redirected
    map.connect("season_schedule", '/nfl/schedule/{season}',
                controller='nfl/schedule', action='season')

    # to be deleted / redirected
    map.connect("week_schedule", '/nfl/schedule/{season}/{week}',
                controller='nfl/schedule', action='week')

    # NFL Games

    # unused (at least for now, might be useful for playoffs)
    map.connect('new_game', '/nfl/games/new',
                controller='nfl/game', action='new')

    # url altered, method changed to POST
    map.connect('create_game', '/nfl/games/create',
                controller='nfl/game', action='create')

    map.connect('edit_game', '/nfl/games/{id}/edit',
                controller='nfl/game', action='edit')

    map.connect('view_games_week', '/nfl/games/')

    map.connect('edit_week', '/nfl/games/{season}/{week}/edit',
                controller='nfl/game', action='edit_for_week')
    map.connect('save_games', '/nfl/games/save',
                controller='nfl/game', action='save_many')

    # url altered, method changed to PUT
    map.connect('save_game', '/nfl/games/{id}/save',
                controller='nfl/game', action='save')

    # GET /nfl/teams
    # GET /nfl/teams/{team}

    ## GET /nfl/seasons/{season}/{week}/games -> all games in the week
    ## GET /nfl/seasons/{season}/{week}/games/{id} -> show game
    ## GET /nfl/seasons/{season}/{week}/games/{id}/edit
    ## GET /nfl/seasons/{season}/{week}/games/edit -> bulk edit games for week

    # GET /nfl/games/schedule/{season} -> weeks

    # GET /nfl/games/schedule/{season}/{week} -> list of game for week (schedule)
    # GET /nfl/games/schedule/{season}/{week}/edit -> edit games for that week
    # PUT /nfl/games/bulk -> bulk update games
    # GET /nfl/games/{id} -> view game


    ## GET /nfl/games -> list of seasons?
    ## GET /nfl/games/{season} -> list of weeks


    # Pickem routes
    # pickem predictions

    map.connect('prediction_season', '/pickem/predictions/{season_id}',
                controller='pickem/prediction', action='season',
                conditions=dict(method=["GET"])
    )

    map.connect('prediction_season_week', '/pickem/predictions/{season_id}/{week}',
                controller='pickem/prediction', action='week',
                conditions=dict(method=["GET"]))

    map.connect('bulk_save_predictions', '/pickem/predictions/bulk',
                controller='pickem/prediction', action='bulk',
                conditions=dict(methpd=["PUT"]))

    # pickem standings

    map.connect("standings", '/pickem/standings/{season}',
                controller="pickem/standings", action="season")

    map.connect("week_standings", "/pickem/standings/{season}/{week}",
                controller="pickem/standings", action="week")

    map.connect("earnings", "/pickem/earnings/{season_id}",
                controller="pickem/earnings", action="index")

    # INTERNAL 'API' ROUTES:
    map.resource('team', 'teams', controller='api/nfl/teams', 
                 path_prefix='/api/nfl', name_prefix='api_nfl_')

    map.resource('game', 'games', controller='api/nfl/games', 
                 path_prefix='/api/nfl', name_prefix='api_nfl_')

    map.resource('prediction', 'predictions', controller='api/pickem/predictions', 
             path_prefix='/api/pickem', name_prefix='api_pickem_')

    return map
