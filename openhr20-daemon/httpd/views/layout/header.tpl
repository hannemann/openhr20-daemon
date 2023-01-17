<header>
    {{ !'<a href="' + base_url + '">&lt;</a>' if 'index' != page else 'OpenHR20' }}
    % include('layout/nav', base_url=base_url)
</header>
