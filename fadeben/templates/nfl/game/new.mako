# -*- coding: utf-8 -*-
<%inherit file="/public.mako"/>

<h1>new game</h1>

${ h.form(url("create_game"), method='post') }

<%include file="form.mako"/>

${ h.submit("submit", "create") }

${ h.end_form() }
