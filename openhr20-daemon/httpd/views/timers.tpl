% import json
% rebase('layout/default', title=title, page='timers')
% header = ['Weekly', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
<div class="thermostat-timers" data-mode="{{ mode }}" data-addr="{{ addr }}">
    <div class="presets--card">
        <h3>Available presets</h3>
        % for preset in presets:
        <div>
            <span>{{ preset['name'] }}:</span>
            <span>{{ int(preset['temp'], 16) / 2 }} °C</span>
        </div>
        % end
    </div>

    <div class="timer-mode--card">
        <h3>Mode</h3>
        <label>One program for every day<input type="radio" name="G22" value="0" {{ 'checked' if mode == 0 else '' }}></label>
        <label>One program per weekday<input type="radio" name="G22" value="1" {{ 'checked' if mode == 1 else '' }}></label>
    </div>

    % for day in range(0, 8):
    % include('./partials/timer-weekday-card', day=day)
    % end

    <div class="timer--card" data-item="actions">
        <button data-action="refresh">Refresh</button>
        <button data-action="save">Save</button>
    </div>
</div>