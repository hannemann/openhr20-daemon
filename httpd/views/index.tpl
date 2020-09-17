    % import json
    % rebase('layout/default', title=title)
    <div class="flex-wrap thermostats">
    <%
        for device in devices:
            include('./partials/thermostat-card', device=device)
    %>
    %end
    </div>

