# -*- coding: utf-8 -*-
<%inherit file="/public.mako"/>

<div class="main-content">
    <h1 style="margin-bottom: 15px;">Earnings calculator</h1>

    <div class="table">
        <div class="header">
            <div>Name</div>
            <div>$</div>
            <div>&Delta;</div>
        </div>
        % for member in c.members:
        <div>
            <div>${ member.first_name }</div>
            <div>${ h.show_money(c.e[ member.id ]) }</div>
            <div>${ h.show_money(c.e[ member.id ] - c.total_spent) }</div>
        </div>
        % endfor
    </div>
          
</div>
