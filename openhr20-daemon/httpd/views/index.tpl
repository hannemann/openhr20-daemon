    % import json
    % rebase('layout/default', title=title, page='index')
    <div class="flex-wrap thermostats">
        % for group in groups:
            <div class="header--group header--card">
                {{ group.name }}
            </div>
            <%
            for device in group.devices:
                include('./partials/thermostat-card', device=device)
            end
            %>
        % end
        % if len(groups) > 0:
        <div class="header--group header--card">
            Ungrouped devices
        </div>
        % end
        <%
        for device in ungrouped_devices:
            include('./partials/thermostat-card', device=device)
        end
        %>
    </div>
