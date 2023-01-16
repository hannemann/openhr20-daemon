<nav>
    <label>
        <input type="checkbox">
        <span class="iconify" data-icon="mdi-menu"></span>
        <span class="iconify" data-icon="mdi-close"></span>
        <span class="click-trap">
            <span class="nav-list">
                <span {{ !' class="active"' if 'index' == page else '' }}>
                    {{ !'<a href="/">' if 'index' != page else '<span>' }}
                      Home
                    {{ !'</a>' if 'index' != page else '</span>'}}
                </span>
                <span {{ !' class="active"' if 'device-manager' == page else '' }}>
                    {{ !'<a href="/device-manager">' if 'device-manager' != page else '<span>' }}
                      Device Manager
                    {{ !'</a>' if 'groups' != page else '</span>'}}
                </span>
            </span>
        </span>
    </label>
</nav>
