# -*- coding: utf-8 -*-
<%inherit file="/public.mako"/>

<h1>edit game</h1>

${ h.form(url("save_game", id=c.game.id), method='post') }

<%include file="form.mako"/>

${ h.submit("submit", "save") }

${ h.end_form() }
