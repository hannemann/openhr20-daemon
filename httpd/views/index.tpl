    % import json
    % rebase('layout/default', title=title)
    <div class="thermostats">
    <%
        for addr, device in devices.items():
            include('./partials/thermostat-card', addr=addr, device=device)
    %>
    %end
    </div>

