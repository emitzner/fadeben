# -*- coding: utf-8 -*-
<%inherit file="/public.mako"/>

zomg it's all the seasons!

<ul>
    % for season in c.seasons:
    <li>${ season.number }</li>
    % endfor
</ul>
