
% type = 'daily_timers' if day == 0 else 'week_timers'
<div class="weekday--card" data-type="{{ type }}">
    <h3>{{ header[day] }}</h3>
    % for slot in range(8):
    % preset = timers[day][slot][0]
    % minutes = int(timers[day][slot][1:4], 16)
    % minute = int(timers[day][slot][1:4], 16) % 60
    % hour = (minutes - (minutes % 60)) / 60 if minutes <= 60 * 24 else 0
    % minute = minute if minutes <= 60 * 24 else 0
    <div class="timer-slot">
        <div class="timer-slot--preset">
            <input type="range" min="0" max="3" id="{{ 't%d%d' % (day, slot) }}" name="{{ 't%d%d' % (day, slot) }}" value="{{ preset }}" list="presets_{{ 't%d%d' % (day, slot) }}">
            <output for="{{ 't%d%d' % (day, slot) }}">{{ int(presets[int(preset)]['temp'], 16) / 2 }}°</output>
            <datalist id="presets_{{ 't%d%d' % (day, slot) }}">
                % for preset in presets:
                <option value="{{ preset['id'] }}" label="{{ int(preset['temp'], 16) / 2 }}°"></option>
                %end
            </datalist>
        </div>
        <input type="time" name="{{ 'v%d%d' % (day, slot) }}" {{ 'value=%0.2d:%0.2d' % (hour, minute) if minutes <= 60 * 24 else '' }}>
    </div>
    % end
</div>