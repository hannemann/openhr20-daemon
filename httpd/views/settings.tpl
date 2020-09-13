% import json
% rebase('layout/default', title=title)
<div class="thermostat-settings">
    % for setting in layout:
    <div class="field">
        <label>{{ setting['name'] }} ({{ hex(setting['idx']) }})</label>
        <input type="text"
               value="{{ device_settings[str(setting['idx'])] if str(setting['idx']) in device_settings else '' }}"
        >
    </div>
    % if 'description' in setting and setting['description'] != '':
    <div class="description">
        {{ setting['description'] }}
    </div>
    % end
    <hr />
    %end
</div>