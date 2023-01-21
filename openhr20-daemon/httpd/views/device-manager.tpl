    % import json
    % import __init__ as daemon
    % rebase('layout/default', title=title, page='device-manager')
    <div class="flex-wrap">
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
        <div class="device-manager" data-devices="{{ str(daemon.devices) }}" data-groups="{{ daemon.devices.__str__(with_remote=False, groups=True) }}">
            <div class="groups">
            </div>
            <div class="header--card">
                Ungrouped Devices
            </div>
            <div class="groups ungrouped-devices">
            </div>
        </div>
    </div>
    <template id="group-template">
        % include('./partials/group-card', group=daemon.Group('', '', []))
    </template>
    <template id="group-device-template">
        % include('./partials/group-card/device', device=daemon.Device(None, '', {}, None, None, None))
    </template>
    <template id="ungrouped-device-template">
        % include('./partials/thermostat-simple', device=daemon.Device(None, '', {}, None, None, None))
    </template>
