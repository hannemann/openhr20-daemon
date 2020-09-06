    % import json
    % rebase('layout', title=title)
    <%
        for addr in devices['names']:
            name = devices.get('names', addr)
            stats = json.loads(devices.get('stats', addr, fallback='{}'))
    %>
    <div>
        <h3>{{ name }}</h3>
        % if 'wanted' in stats:
                Wanted: {{ stats["wanted"] }}
        % end

    </div>

