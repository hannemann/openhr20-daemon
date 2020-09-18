    % import json
    % from Group import Group
    % from Device import Device
    % rebase('layout/default', title=title)
    <div class="header--group header--card">
        <span>Groups</span>
        <span class="action-icon">
            <label>
                <span class="iconify" data-icon="mdi-plus-outline"></span>
                <input type="checkbox">
                <span class="add-input">
                    <input>
                    <span class="action-icon">
                        <span class="iconify" data-icon="mdi-check-outline"></span>
                    </span>
                    <span class="action-icon">
                        <span class="iconify" data-icon="mdi-close-outline"></span>
                    </span>
                </span>
            </label>
        </span>
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

    <template id="group-template">
        % include('./partials/group-card', group=Group('', []))
    </template>
    <template id="group-device-template">
        % include('./partials/group-card/device', device=Device(None, '', {}, None, None, None))
    </template>