    % import json
    % rebase('layout/default', title=title)
    <div class="header--card">
        Groups
    </div>
    <div class="flex-wrap groups">
        <%
            for group in groups:
                include('./partials/group-card', group=group)
            end
        %>
    </div>
    <div class="header--card">
        Ungrouped Devices
    </div>
    <div class="flex-wrap groups">
        <%
            for device in ungrouped_devices:
                include('./partials/thermostat-simple')
            end
        %>
    </div>
