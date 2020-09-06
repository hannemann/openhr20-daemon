<div class="thermostat-card">
    <h3>
        <span class="iconify" data-icon="mdi-home-thermometer-outline"></span>
        {{ device['name'] }}
    </h3>
    % if 'wanted' in device['stats']:
    <div class="thermostat-card--wanted">Wanted: {{ device['stats']["wanted"] }}</div>
    % end
    % if 'real' in device['stats']:
    <div class="thermostat-card--real">Real: {{ device['stats']["real"] }}</div>
    % end
    % if 'valve' in device['stats']:
    <div class="thermostat-card--valve">Valve: {{ device['stats']["valve"] }}</div>
    % end
    % if 'battery' in device['stats']:
    <div class="thermostat-card--battery">Battery: {{ device['stats']["battery"] }}</div>
    % end
    % if 'synced' in device['stats']:
    <div class="thermostat-card--synced">Synced: {{ device['stats']["synced"] }}</div>
    % end
</div>