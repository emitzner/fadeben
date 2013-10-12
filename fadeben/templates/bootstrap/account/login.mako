# -*- coding: utf-8 -*-
<%inherit file="/bootstrap/public.mako"/>

<form class="form-signin" action="${ url('login', next=request.GET.get('next') or '/') }" method="POST">
    <h2 class="form-signin-heading">Please sign in</h2>
    <input type="text" class="form-control" placeholder="Email address" name="username" autofocus>
    <input type="password" class="form-control" placeholder="Password" name="password">
    <label class="checkbox">
        <input type="checkbox" value="remember-me"> Remember me
    </label>
    <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
</form>
