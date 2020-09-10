%from datetime import datetime
<div class="thermostat-card"
     data-name="{{ device['name'] }}"
     % for attr in device['stats']:
         data-{{attr}}="{{ str(device['stats'][attr]).lower() }}"
    % end
>
    <h3>
        <span class="iconify" data-icon="mdi-home-thermometer-outline"></span>
        <span>{{ device['name'] }}</span>
        <span class="update-button">
            <span class="iconify" data-icon="mdi-update"></span>
        </span>
        % if 'time' in device['stats']:
        <span data-item="time">
            {{ datetime.fromtimestamp(device['stats']['time']).strftime('%d.%m.%Y %H:%M:%S') }}
        </span>
        %end
    </h3>
    % if 'mode' in device['stats']:
    <div class="thermostat-card--item" data-item="mode">
        <span>Mode</span>
        <span class="value-display mode-button">
            <span class="mode-manu">
                <span class="iconify" data-icon="mdi-hand-left"></span>
            </span>
            <span class="mode-auto">
                <span class="iconify" data-icon="mdi-calendar-clock"></span>
            </span>
            <span class="mode--">
                -
            </span>
        </span>
    </div>
    % end
    % if 'wanted' in device['stats']:
    <div class="thermostat-card--item" data-item="wanted">
        <label for="{{ device['stats']["addr"] }}-wanted">
            Wanted:
        </label>
        <input id="{{ device['stats']["addr"] }}-wanted" type="range" step="0.5" min="5" max="30" value="{{ device['stats']["wanted"] }}">
        <span class="value-display"><span>{{ device['stats']["wanted"] }}</span> °C</span>
    </div>
    % end
    % if 'real' in device['stats']:
    <div class="thermostat-card--item" data-item="real">
        <span>Real:</span>
        <span class="value-display"><span>{{ device['stats']["real"] }}</span> °C</span>
    </div>
    % end
    % if 'valve' in device['stats']:
    <div class="thermostat-card--item" data-item="valve">
        <span>Valve:</span>
        <span class="value-display"><span>{{ device['stats']["valve"] }}</span> %</span>
    </div>
    % end
    % if 'battery' in device['stats']:
    <div class="thermostat-card--item" data-item="battery">
        <span>Battery:</span>
        <span class="value-display"><span>{{ device['stats']["battery"] }}</span> V</div>
    % end
    % if 'synced' in device['stats']:
    <div class="thermostat-card--item" data-item="synced">
        <span>Synced:</span>
        <span class="value-display">
            <span class="synced">
                <span class="iconify" data-icon="mdi-check-box-outline"></span>
            </span>
            <span class="not-synced">
                <span class="iconify" data-icon="mdi-checkbox-blank-outline"></span>
            </span>
        </span>
    </div>
    % end
    <span class="loading">
        <span class="iconify" data-icon="mdi-loading"></span>
    </span>
</div>