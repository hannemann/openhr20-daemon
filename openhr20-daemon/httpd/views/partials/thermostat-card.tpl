%from datetime import datetime
% import os
% base_url = os.getenv("BASE_URL", default='/')
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
        <svg data-icon="mdi-home-thermometer-outline" style="width:1em;height:1em" viewBox="0 0 24 24">
            <path fill="currentColor" d="M19 8C20.11 8 21 8.9 21 10V16.76C21.61 17.31 22 18.11 22 19C22 20.66 20.66 22 19 22C17.34 22 16 20.66 16 19C16 18.11 16.39 17.31 17 16.76V10C17 8.9 17.9 8 19 8M19 9C18.45 9 18 9.45 18 10V11H20V10C20 9.45 19.55 9 19 9M12 5.69L7 10.19V18H14.1L14 19L14.1 20H5V12H2L12 3L16.4 6.96C15.89 7.4 15.5 7.97 15.25 8.61L12 5.69Z" />
        </svg>
        <span>{{ device.name }}</span>
        <span class="update-button">
            <svg data-icon="mdi-update" style="width:1em;height:1em" viewBox="0 0 24 24">
                <path fill="currentColor" d="M21,10.12H14.22L16.96,7.3C14.23,4.6 9.81,4.5 7.08,7.2C4.35,9.91 4.35,14.28 7.08,17C9.81,19.7 14.23,19.7 16.96,17C18.32,15.65 19,14.08 19,12.1H21C21,14.08 20.12,16.65 18.36,18.39C14.85,21.87 9.15,21.87 5.64,18.39C2.14,14.92 2.11,9.28 5.62,5.81C9.13,2.34 14.76,2.34 18.27,5.81L21,3V10.12M12.5,8V12.25L16,14.33L15.28,15.54L11,13V8H12.5Z" />
            </svg>
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
                    <svg data-icon="mdi-hand-left" style="width:1em;height:1em" viewBox="0 0 24 24">
                        <path fill="currentColor" d="M3 16V5.75C3 5.06 3.56 4.5 4.25 4.5S5.5 5.06 5.5 5.75V12H6.5V2.75C6.5 2.06 7.06 1.5 7.75 1.5C8.44 1.5 9 2.06 9 2.75V12H10V1.25C10 .56 10.56 0 11.25 0S12.5 .56 12.5 1.25V12H13.5V3.25C13.5 2.56 14.06 2 14.75 2S16 2.56 16 3.25V15H16.75L18.16 11.47C18.38 10.92 18.84 10.5 19.4 10.31L20.19 10.05C21 9.79 21.74 10.58 21.43 11.37L18.4 19C17.19 22 14.26 24 11 24C6.58 24 3 20.42 3 16Z" />
                    </svg>
                </span>
                <span class="mode-auto">
                    <svg data-icon="mdi-calendar-clock" style="width:1em;height:1em" viewBox="0 0 24 24">
                        <path fill="currentColor" d="M15,13H16.5V15.82L18.94,17.23L18.19,18.53L15,16.69V13M19,8H5V19H9.67C9.24,18.09 9,17.07 9,16A7,7 0 0,1 16,9C17.07,9 18.09,9.24 19,9.67V8M5,21C3.89,21 3,20.1 3,19V5C3,3.89 3.89,3 5,3H6V1H8V3H16V1H18V3H19A2,2 0 0,1 21,5V11.1C22.24,12.36 23,14.09 23,16A7,7 0 0,1 16,23C14.09,23 12.36,22.24 11.1,21H5M16,11.15A4.85,4.85 0 0,0 11.15,16C11.15,18.68 13.32,20.85 16,20.85A4.85,4.85 0 0,0 20.85,16C20.85,13.32 18.68,11.15 16,11.15Z" />
                    </svg>
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
                <svg data-icon="mdi-check-box-outline" style="width:1em;height:1em" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M19,3H5A2,2 0 0,0 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5A2,2 0 0,0 19,3M19,5V19H5V5H19M10,17L6,13L7.41,11.58L10,14.17L16.59,7.58L18,9" />
                </svg>
            </span>
            <span class="not-synced">
                <svg data-icon="mdi-checkbox-blank-outline" style="width:1em;height:1em" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M19,3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3M19,5V19H5V5H19Z" />
                </svg>
            </span>
        </span>
    </div>
    <div class="thermostat--card--item" data-item="error">
        <span class="label">Error</span>
        <span class="value-display">
            <span class="error-icon" data-error="4" data-descr="Montage">
                <svg data-icon="mdi-cog-refresh-outline" style="width:1em;height:1em" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M18 14.5C19.1 14.5 20.1 14.9 20.8 15.7L22 14.5V18.5H18L19.8 16.7C19.3 16.3 18.7 16 18 16C16.6 16 15.5 17.1 15.5 18.5S16.6 21 18 21C18.8 21 19.5 20.6 20 20H21.7C21.1 21.5 19.7 22.5 18 22.5C15.8 22.5 14 20.7 14 18.5S15.8 14.5 18 14.5M11.7 20H11.3L10.9 17.4C9.7 17.2 8.7 16.5 7.9 15.6L5.5 16.6L4.7 15.3L6.8 13.7C6.4 12.5 6.4 11.3 6.8 10.1L4.7 8.7L5.5 7.4L7.9 8.4C8.7 7.5 9.7 6.9 10.9 6.6L11.2 4H12.7L13.1 6.6C14.3 6.8 15.4 7.5 16.1 8.4L18.5 7.4L19.3 8.7L17.2 10.2C17.4 10.8 17.5 11.4 17.5 12H18C18.5 12 19 12.1 19.5 12.2V12L19.4 11L21.5 9.4C21.7 9.2 21.7 9 21.6 8.8L19.6 5.3C19.5 5 19.3 5 19 5L16.5 6C16 5.6 15.4 5.3 14.8 5L14.4 2.3C14.5 2.2 14.2 2 14 2H10C9.8 2 9.5 2.2 9.5 2.4L9.1 5.1C8.5 5.3 8 5.7 7.4 6L5 5C4.7 5 4.5 5 4.3 5.3L2.3 8.8C2.2 9 2.3 9.2 2.5 9.4L4.6 11L4.5 12L4.6 13L2.5 14.7C2.3 14.9 2.3 15.1 2.4 15.3L4.4 18.8C4.5 19 4.7 19 5 19L7.5 18C8 18.4 8.6 18.7 9.2 19L9.6 21.7C9.6 21.9 9.8 22.1 10.1 22.1H12.6C12.1 21.4 11.9 20.7 11.7 20M16 12.3V12C16 9.8 14.2 8 12 8S8 9.8 8 12C8 14.2 9.8 16 12 16C12.7 14.3 14.2 12.9 16 12.3M10 12C10 10.9 10.9 10 12 10S14 10.9 14 12 13.1 14 12 14 10 13.1 10 12Z" />
                </svg>
            </span>
            <span class="error-icon" data-error="8" data-descr="Motor">
                <svg data-icon="mdi-cog-off-outline" style="width:1em;height:1em" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M22.11 21.46L2.39 1.73L1.11 3L4 5.88L2.34 8.73C2.21 8.95 2.27 9.22 2.46 9.37L4.57 11L4.5 12L4.57 12.97L2.46 14.63C2.27 14.78 2.21 15.05 2.34 15.27L4.34 18.73C4.46 18.95 4.73 19.03 4.95 18.95L7.44 17.94C7.96 18.34 8.5 18.68 9.13 18.93L9.5 21.58C9.54 21.82 9.75 22 10 22H14C14.25 22 14.46 21.82 14.5 21.58L14.87 18.93C15.38 18.73 15.83 18.45 16.26 18.15L20.84 22.73L22.11 21.46M10 11.9L12.1 14C12.06 14 12.03 14 12 14C10.9 14 10 13.11 10 12C10 11.97 10 11.94 10 11.9M13.13 17.39L12.76 20H11.24L10.87 17.38C9.68 17.14 8.63 16.5 7.86 15.62L5.43 16.66L4.68 15.36L6.8 13.8C6.4 12.64 6.4 11.37 6.8 10.2L4.69 8.65L5.44 7.35L5.5 7.37L8.4 10.29C8.15 10.8 8 11.38 8 12C8 14.21 9.79 16 12 16C12.62 16 13.2 15.86 13.71 15.6L14.83 16.72C14.31 17.03 13.74 17.26 13.13 17.39M10.06 6.86L8.55 5.35C8.74 5.26 8.93 5.15 9.13 5.07L9.5 2.42C9.54 2.18 9.75 2 10 2H14C14.25 2 14.46 2.18 14.5 2.42L14.87 5.07C15.5 5.32 16.04 5.66 16.56 6.05L19.05 5.05C19.27 4.96 19.54 5.05 19.66 5.27L21.66 8.73C21.79 8.95 21.73 9.22 21.54 9.37L19.43 11L19.5 12L19.43 13L21.54 14.63C21.73 14.78 21.79 15.05 21.66 15.27L20.5 17.29L19.04 15.84L19.32 15.36L17.2 13.81C17.6 12.64 17.6 11.37 17.2 10.2L19.31 8.65L18.56 7.35L16.15 8.39C15.38 7.5 14.32 6.86 13.12 6.62L12.75 4H11.25L10.88 6.61C10.6 6.67 10.32 6.75 10.06 6.86M12 8C14.21 8 16 9.79 16 12C16 12.25 15.97 12.5 15.93 12.73L11.27 8.07C11.5 8.03 11.75 8 12 8Z" />
                </svg>
            </span>
            <span class="error-icon" data-error="16" data-descr="RFM">
                <svg data-icon="mdi-access-point-off" style="width:1em;height:1em" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M20.84 22.73L12.1 14C12.06 14 12.03 14 12 14C10.9 14 10 13.11 10 12C10 11.97 10 11.94 10 11.9L8.4 10.29C8.15 10.81 8 11.38 8 12C8 13.11 8.45 14.11 9.17 14.83L7.76 16.24C6.67 15.15 6 13.65 6 12C6 10.83 6.34 9.74 6.93 8.82L5.5 7.37C4.55 8.67 4 10.27 4 12C4 14.22 4.89 16.22 6.34 17.66L4.93 19.07C3.12 17.26 2 14.76 2 12C2 9.72 2.77 7.63 4.06 5.95L1.11 3L2.39 1.73L22.11 21.46L20.84 22.73M15.93 12.73L17.53 14.33C17.83 13.61 18 12.83 18 12C18 10.35 17.33 8.85 16.24 7.76L14.83 9.17C15.55 9.89 16 10.89 16 12C16 12.25 15.97 12.5 15.93 12.73M19.03 15.83L20.5 17.28C21.44 15.75 22 13.94 22 12C22 9.24 20.88 6.74 19.07 4.93L17.66 6.34C19.11 7.78 20 9.79 20 12C20 13.39 19.65 14.7 19.03 15.83Z" />
                </svg>
            </span>
            <span class="error-icon" data-error="64" data-descr="Battery warn">
                <svg data-icon="mdi-battery-alert-variant-outline" style="width:1em;height:1em" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M14 20H6V6H14M14.67 4H13V2H7V4H5.33C4.6 4 4 4.6 4 5.33V20.67C4 21.4 4.6 22 5.33 22H14.67C15.4 22 16 21.4 16 20.67V5.33C16 4.6 15.4 4 14.67 4M21 7H19V13H21V8M21 15H19V17H21V15Z" />
                </svg>
            </span>
            <span class="error-icon" data-error="128" data-descr="Battery error">
                <svg data-icon="mdi-battery-off-outline" style="width:1em;height:1em" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M18 17.35L3.38 2.73L2.11 4L6 7.89V20.67A1.34 1.34 0 0 0 7.33 22H16.67A1.34 1.34 0 0 0 18 20.67V19.89L20.84 22.73L22.11 21.46M16 20H8V9.89L16 17.89M16 6V12.8L18 14.8V5.33A1.34 1.34 0 0 0 16.67 4H15V2H9V4H7.21L9.21 6Z" />
                </svg>
            </span>
            <span class="error-icon" data-error="256" data-descr="Offline">
                <svg data-icon="mdi-access-point-off" style="width:1em;height:1em" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M20.84 22.73L12.1 14C12.06 14 12.03 14 12 14C10.9 14 10 13.11 10 12C10 11.97 10 11.94 10 11.9L8.4 10.29C8.15 10.81 8 11.38 8 12C8 13.11 8.45 14.11 9.17 14.83L7.76 16.24C6.67 15.15 6 13.65 6 12C6 10.83 6.34 9.74 6.93 8.82L5.5 7.37C4.55 8.67 4 10.27 4 12C4 14.22 4.89 16.22 6.34 17.66L4.93 19.07C3.12 17.26 2 14.76 2 12C2 9.72 2.77 7.63 4.06 5.95L1.11 3L2.39 1.73L22.11 21.46L20.84 22.73M15.93 12.73L17.53 14.33C17.83 13.61 18 12.83 18 12C18 10.35 17.33 8.85 16.24 7.76L14.83 9.17C15.55 9.89 16 10.89 16 12C16 12.25 15.97 12.5 15.93 12.73M19.03 15.83L20.5 17.28C21.44 15.75 22 13.94 22 12C22 9.24 20.88 6.74 19.07 4.93L17.66 6.34C19.11 7.78 20 9.79 20 12C20 13.39 19.65 14.7 19.03 15.83Z" />
                </svg>
            </span>
        </span>
    </div>
    <div class="thermostat--card--item" data-item="actions">
        <a href="{{ base_url }}settings/{{ device.addr}}">
            <svg data-icon="mdi-cog-outline" style="width:1em;height:1em" viewBox="0 0 24 24">
                <path fill="currentColor" d="M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8M12,10A2,2 0 0,0 10,12A2,2 0 0,0 12,14A2,2 0 0,0 14,12A2,2 0 0,0 12,10M10,22C9.75,22 9.54,21.82 9.5,21.58L9.13,18.93C8.5,18.68 7.96,18.34 7.44,17.94L4.95,18.95C4.73,19.03 4.46,18.95 4.34,18.73L2.34,15.27C2.21,15.05 2.27,14.78 2.46,14.63L4.57,12.97L4.5,12L4.57,11L2.46,9.37C2.27,9.22 2.21,8.95 2.34,8.73L4.34,5.27C4.46,5.05 4.73,4.96 4.95,5.05L7.44,6.05C7.96,5.66 8.5,5.32 9.13,5.07L9.5,2.42C9.54,2.18 9.75,2 10,2H14C14.25,2 14.46,2.18 14.5,2.42L14.87,5.07C15.5,5.32 16.04,5.66 16.56,6.05L19.05,5.05C19.27,4.96 19.54,5.05 19.66,5.27L21.66,8.73C21.79,8.95 21.73,9.22 21.54,9.37L19.43,11L19.5,12L19.43,13L21.54,14.63C21.73,14.78 21.79,15.05 21.66,15.27L19.66,18.73C19.54,18.95 19.27,19.04 19.05,18.95L16.56,17.95C16.04,18.34 15.5,18.68 14.87,18.93L14.5,21.58C14.46,21.82 14.25,22 14,22H10M11.25,4L10.88,6.61C9.68,6.86 8.62,7.5 7.85,8.39L5.44,7.35L4.69,8.65L6.8,10.2C6.4,11.37 6.4,12.64 6.8,13.8L4.68,15.36L5.43,16.66L7.86,15.62C8.63,16.5 9.68,17.14 10.87,17.38L11.24,20H12.76L13.13,17.39C14.32,17.14 15.37,16.5 16.14,15.62L18.57,16.66L19.32,15.36L17.2,13.81C17.6,12.64 17.6,11.37 17.2,10.2L19.31,8.65L18.56,7.35L16.15,8.39C15.38,7.5 14.32,6.86 13.12,6.62L12.75,4H11.25Z" />
            </svg>
        </a>
        <a href="{{ base_url }}timers/{{ device.addr}}">
            <svg data-icon="mdi-calendar" style="width:1em;height:1em" viewBox="0 0 24 24">
                <path fill="currentColor" d="M19,19H5V8H19M16,1V3H8V1H6V3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3H18V1M17,12H12V17H17V12Z" />
            </svg>
        </a>
    </div>
    <span class="loading">
        <svg data-icon="mdi-loading" style="width:1em;height:1em" viewBox="0 0 24 24">
            <path fill="currentColor" d="M12,4V2A10,10 0 0,0 2,12H4A8,8 0 0,1 12,4Z" />
        </svg>
        <span class="cancel">
            <svg data-icon="mdi-close" style="width:1em;height:1em" viewBox="0 0 24 24">
                <path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" />
            </svg>
        </span>
    </span>
</div>