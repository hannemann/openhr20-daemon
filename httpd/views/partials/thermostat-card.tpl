%from datetime import datetime
<div class="thermostat--card"
     data-name="{{ device.name }}"
     % for attr, value in device.get_stats().items():
         data-{{attr}}="{{ str(value).lower() }}"
    % end
>
    <h3>
        <span class="iconify" data-icon="mdi-home-thermometer-outline"></span>
        <span>{{ device.name }}</span>
        <span class="update-button">
            <span class="iconify" data-icon="mdi-update"></span>
        </span>
        <span data-item="time">
            {{ datetime.fromtimestamp(device.time).strftime('%d.%m.%Y %H:%M:%S') }}
        </span>
    </h3>
    <div class="thermostat--card--item" data-item="mode">
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
    <div class="thermostat--card--item" data-item="wanted">
        <label for="{{ device.addr }}-wanted">
            Wanted:
        </label>
        <input id="{{ device.addr }}-wanted" type="range" step="0.5" min="5" max="30" value="{{ device.wanted }}">
        <span class="value-display"><span>{{ device.wanted }}</span> °C</span>
    </div>
    <div class="thermostat--card--item" data-item="real">
        <span>Real:</span>
        <span class="value-display"><span>{{ device.real }}</span> °C</span>
    </div>
    <div class="thermostat--card--item" data-item="valve">
        <span>Valve:</span>
        <span class="value-display"><span>{{ device.valve }}</span> %</span>
    </div>
    <div class="thermostat--card--item" data-item="battery">
        <span>Battery:</span>
        <span class="value-display"><span>{{ device.battery }}</span> V
    </div>
    <div class="thermostat--card--item" data-item="synced">
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
    <div class="thermostat--card--item" data-item="actions">
        <a href="/settings/{{ device.addr}}">
            <span class="iconify" data-icon="mdi-cog-outline"></span>
        </a>
        <a href="/timers/{{ device.addr}}">
            <span class="iconify" data-icon="mdi-calendar"></span>
        </a>
    </div>
    <span class="loading">
        <span class="iconify" data-icon="mdi-loading"></span>
    </span>
</div>