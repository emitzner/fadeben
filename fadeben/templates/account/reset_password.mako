# -*- coding: utf-8 -*-
<%inherit file="/public.mako"/>

<div class="main-content">
	<h1>Reset Password</h1>

	${ h.form(url('reset_password'), method="post") }
	<fieldset>
		<label for="email">Email:</label>
		${ h.text('email') }<br>
	</fieldset>
	${ h.submit("submit", "Reset Password") }<br>
	${ h.end_form() }
</div>
