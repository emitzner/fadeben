# -*- coding: utf-8 -*-
<%inherit file="/public.mako"/>

<div class="main-content">
	<h1>Change Password</h1>

	${ h.form(url('change_password_submit'), method="post") }
	<fieldset>
		<label for="old_password">Current password:</label>
		${ h.password('old_password') }<br>
		<label for="new_password1">New password:</label>
		${ h.password('new_password1') }<br>
		<label for="new_password2">Confirm password:</label>
		${ h.password('new_password2') }<br>
	</fieldset>
	${ h.submit("submit", "Change Password") }<br>
	${ h.end_form() }
</div>
