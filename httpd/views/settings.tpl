% import json
% rebase('layout/default', title=title)
<div class="thermostat-settings">
    % for setting in layout:
    <div class="setting">
        <label>
            <span>({{ '0x%s' % setting['idx'] }})</span>
            {{ setting['name'] }}
        </label>
        <div class="field">
            <div>
                <input name="{{ setting['idx'] }}" type="range" min="{{ setting['range'][0] }}" max="{{ setting['range'][1] }}"
                       {{ 'readonly disabled' if 'readonly' in setting and setting['readonly'] == True else '' }}
                       value="{{ int(device_settings[setting['idx']], 16) if setting['idx'] in device_settings else '' }}"
                       oninput="this.closest('.field').querySelector('span').dataset.int = this.value;this.closest('.field').querySelector('span').dataset.hex = `(0x${this.valueAsNumber.toString(16).padStart(2, '0')})`"
                >
            </div>
            <span data-int="{{ int(device_settings[setting['idx']], 16) if setting['idx'] in device_settings else '' }}"
                  data-hex="(0x{{ device_settings[setting['idx']] if setting['idx'] in device_settings else '' }})"></span>
        </div>
        % if 'description' in setting and setting['description'] != '':
        <div class="description">
            {{ setting['description'] }}
        </div>
        % end
    </div>
    %end
</div>