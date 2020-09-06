    % import json
    % rebase('layout/default', title=title)
    <%
        for addr in devices['names']:
            name = devices.get('names', addr)
            stats = json.loads(devices.get('stats', addr, fallback='{}'))
            include('./partials/thermostat-card', stats=stats, name=name)
    %>
    %end

