<div class="thermostat-card">
    <h3>
        <span class="iconify" data-icon="mdi-home-thermometer-outline"></span>
        {{ name }}
    </h3>
    % if 'wanted' in stats:
    <div class="thermostat-card--wanted">Wanted: {{ stats["wanted"] }}</div>
    % end
    % if 'real' in stats:
    <div class="thermostat-card--real">Real: {{ stats["real"] }}</div>
    % end
    % if 'valve' in stats:
    <div class="thermostat-card--valve">Valve: {{ stats["valve"] }}</div>
    % end
    % if 'battery' in stats:
    <div class="thermostat-card--battery">Battery: {{ stats["battery"] }}</div>
    % end
    % if 'synced' in stats:
    <div class="thermostat-card--synced">Synced: {{ stats["synced"] }}</div>
    % end
</div>