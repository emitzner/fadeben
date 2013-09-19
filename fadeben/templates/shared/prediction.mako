<%page args="game,pred=None"/>
<table class="display-table natural-width choose-team" data-game-id="${ game.id }">
    <thead>
        <tr>
            <th>${ game.game_time_l.strftime("%a %m/%d %I:%M") }</th>
            <th>Team</th>
            <th>+/-</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="selector">${ h.radio("prediction-{0}".format(game.id), False, id="game-{0}-away".format(game.id), checked=(pred is False)) }</td>
            <td class="team"><label for="game-${ game.id }-away">${ game.away_team.name }</label></td>
            <td class="spread" rowspan="2">${ h.show_spread(game.spread) }</td>
        </tr>
        <tr>
            <td class="selector">${ h.radio("prediction-{0}".format(game.id), True, id="game-{0}-home".format(game.id), checked=(pred is True)) }</td>
            <td class="team"><label for="game-${ game.id }-home">${ game.home_team.name }</label></td>
        </tr>
    </tbody>
</table>
