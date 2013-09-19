# -*- coding: utf-8 -*-
${ h.select("season",[], [x.number for x in c.seasons]) }
<br>
${ h.select('week', [], range(1, 18)) }
<br>
${ h.select('away_team_id', 1,
            [(x.id, x.name) for x in c.teams]) }
<br>
${ h.select('home_team_id', 2,
            [(x.id, x.name) for x in c.teams]) }
<br>
${ h.text('away_score', '') }
<br>
${ h.text('home_score', '') }
<br>
${ h.text("spread", "") }
<br>

