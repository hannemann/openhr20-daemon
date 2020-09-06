    % import json
    % rebase('layout/default', title=title)
    <%
        for addr, device in devices.items():
            include('./partials/thermostat-card', addr=addr, device=device)
    %>
    %end

