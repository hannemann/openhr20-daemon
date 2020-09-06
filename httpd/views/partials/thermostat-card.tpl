<div class="thermostat-card">
    <h3>
        <span class="iconify" data-icon="mdi-home-thermometer-outline"></span>
        {{ device['name'] }}
    </h3>
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
    <div class="thermostat-card--item" data-item="valve">Valve: {{ device['stats']["valve"] }}</div>
    % end
    % if 'battery' in device['stats']:
    <div class="thermostat-card--item" data-item="battery">Battery: {{ device['stats']["battery"] }}</div>
    % end
    % if 'synced' in device['stats']:
    <div class="thermostat-card--item" data-item="synced">Synced: {{ device['stats']["synced"] }}</div>
    % end
</div>