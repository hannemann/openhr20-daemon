
<div class="timer-slot">
    <div class="timer-slot--preset">
        <input type="range" min="0" max="3" id="{{ 't{}{}'.format(day, slot) }}" name="{{ 't{}{}'.format(day, slot) }}" value="{{ preset }}" list="presets_{{ 't{}{}'.format(day, slot) }}">
        <output for="{{ 't{}{}'.format(day, slot) }}">{{ int(presets[int(preset)]['temp'], 16) / 2 }}°</output>
        <datalist id="presets_{{ 't{}{}'.format(day, slot) }}">
            % for preset in presets:
            <option value="{{ preset['id'] }}" label="{{ int(preset['temp'], 16) / 2 }}°"></option>
            %end
        </datalist>
    </div>
    <div class="timer-slot--time">
        <span class="timer-delete">
            <span class="iconify" data-icon="mdi-close"></span>
        </span>
        <input type="time" name="{{ 'v{}{}'.format(day, slot) }}" {{ 'value={:02d}:{:02d}'.format(hour, minute) if minutes <= 60 * 24 else '' }}>
    </div>
</div>