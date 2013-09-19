# -*- coding: utf-8 -*-
<%inherit file="/mobile/public.mako"/>

<div data-ajax="false">
    ${ h.form(
    url("login", next=(request.GET.get('next') or '/')),
    method="post"
    )
    }
    <label for="username" class="ui-hidden-accessible">
        Username:
    </label>
    ${ h.text('username', placeholder='Username') }
    <label for="password" class="ui-hidden-accessible">
        Password:
    </label>
    ${ h.password('password', placeholder='Password') }

    <button type="submit" data-theme="a">Login</button>

    ${ h.end_form() }

</div>

<%def name="header_text()">
Login
</%def>
