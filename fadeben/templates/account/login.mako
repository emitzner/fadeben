# -*- coding: utf-8 -*-
<%inherit file="/public.mako"/>

<div class="main-content">
	<h1>Login</h1>
	${ h.form(url("login", next=(request.GET.get('next') or '/'), method="post")) }
	<fieldset>
		<label for="username">Username:</label>
		${ h.text('username') }<br>
		<label for="password">Password:</label>
		${ h.password('password') }<br>
		<label for="remember_me">Stay signed in?</label>
		${ h.checkbox("remember_me", checked=True) }<br>
	</fieldset>
	${ h.submit('login_submit', 'Login') }
	${ h.end_form() }
</div>
