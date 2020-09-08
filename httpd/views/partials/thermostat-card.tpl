<div class="thermostat-card" data-name="{{ device['name'] }}" data-addr="{{ device['stats']['addr'] if 'addr' in device['stats'] else '' }}">
    <h3>
        <span class="iconify" data-icon="mdi-home-thermometer-outline"></span>
        {{ device['name'] }}
    </h3>
    % if 'mode' in device['stats']:
    <div class="thermostat-card--item" data-item="mode">
        % if device['stats']["mode"] == 'MANU':
        <span class="iconify" data-icon="mdi-hand-left"></span>
        % else:
        <span class="iconify" data-icon="mdi-calendar-clock"></span>
        %end
    </div>
    %end
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
        <span>{{ device['stats']["real"] }} °C</span>
    </div>
    % end
    % if 'valve' in device['stats']:
    <div class="thermostat-card--item" data-item="valve">
        <span>Valve:</span>
        <span>{{ device['stats']["valve"] }}</span>
    </div>
    % end
    % if 'battery' in device['stats']:
    <div class="thermostat-card--item" data-item="battery">Battery: {{ device['stats']["battery"] }}</div>
    % end
    % if 'synced' in device['stats']:
    <div class="thermostat-card--item" data-item="synced">Synced: {{ device['stats']["synced"] }}</div>
    % end
</div>