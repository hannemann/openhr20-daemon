%from datetime import datetime
% antifreeze = int(device.settings[device.PRESET_ANTIFREEZE_SETTING], 16) / 2 if device.PRESET_ANTIFREEZE_SETTING in device.settings else 0
% eco = int(device.settings[device.PRESET_ECO_SETTING], 16) / 2 if device.PRESET_ECO_SETTING in device.settings else 0
% comfort = int(device.settings[device.PRESET_COMFORT_SETTING], 16) / 2 if device.PRESET_COMFORT_SETTING in device.settings else 0
% supercomfort = int(device.settings[device.PRESET_SUPERCOMFORT_SETTING], 16) / 2 if device.PRESET_SUPERCOMFORT_SETTING in device.settings else 0
<div class="thermostat--card"
     data-name="{{ device.name }}"
     % for attr, value in device.dict().items():
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
    <div class="control">
        <div class="thermostat--card--item" data-item="mode">
            <span class="label">Mode</span>
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
            <span class="wanted-control">
                <input id="{{ device.addr }}-wanted" type="range" step="0.5" min="5" max="30" value="{{ device.wanted }}">
            </span>
            <span class="value-display" data-is-current="true"><span>{{ device.wanted }}</span> °C</span>
        </div>
        <div class="thermostat--card--item" data-item="presets">
            <span class="label">Preset:</span>
            <span class="value-display">
                <span class="preset" data-preset="antifreeze" data-temperature="{{ antifreeze }}">{{ antifreeze }}</span>
                <span class="preset" data-preset="eco" data-temperature="{{ eco }}">{{ eco }}</span>
                <span class="preset" data-preset="comfort" data-temperature="{{ comfort }}">{{ comfort }}</span>
                <span class="preset" data-preset="supercomfort" data-temperature="{{ supercomfort }}">{{ supercomfort }}</span>
            </span>
        </div>
    </div>

    <div class="data">
        <div class="thermostat--card--item" data-item="real">
            <span class="label">Real:</span>
            <span class="value-display"><span>{{ device.real }}</span> °C</span>
        </div>
        <div class="thermostat--card--item" data-item="valve">
            <span class="label">Valve:</span>
            <span class="value-display"><span>{{ device.valve }}</span> %</span>
        </div>
        <div class="thermostat--card--item" data-item="battery">
            <span class="label">Battery:</span>
            <span class="value-display"><span>{{ device.battery }}</span> V
        </div>
    </div>
    <div class="thermostat--card--item" data-item="synced">
        <span class="label">Synced:</span>
        <span class="value-display">
            <span class="synced">
                <span class="iconify" data-icon="mdi-check-box-outline"></span>
            </span>
            <span class="not-synced">
                <span class="iconify" data-icon="mdi-checkbox-blank-outline"></span>
            </span>
        </span>
    </div>
    <div class="thermostat--card--item" data-item="error">
        <span class="label">Error</span>
        <span class="value-display">
            <span class="error-icon" data-error="4" data-descr="Montage">
                <span class="iconify" data-icon="mdi-cog-refresh-outline"></span>
            </span>
            <span class="error-icon" data-error="8" data-descr="Motor">
                <span class="iconify" data-icon="mdi-cog-off-outline"></span>
            </span>
            <span class="error-icon" data-error="16" data-descr="RFM">
                <span class="iconify" data-icon="mdi-access-point-off"></span>
            </span>
            <span class="error-icon" data-error="64" data-descr="Battery warn">
                <span class="iconify" data-icon="mdi-battery-alert-variant-outline"></span>
            </span>
            <span class="error-icon" data-error="128" data-descr="Battery error">
                <span class="iconify" data-icon="mdi-battery-off-outline"></span>
            </span>
            <span class="error-icon" data-error="256" data-descr="Offline">
                <span class="iconify" data-icon="mdi-access-point-off"></span>
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
        <span class="cancel">
            <span class="iconify" data-icon="mdi-close"></span>
        </span>
    </span>
</div>