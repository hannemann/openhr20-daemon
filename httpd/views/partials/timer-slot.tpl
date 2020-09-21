
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
    <div class="timer-slot--time">
        <span class="timer-delete">
            <span class="iconify" data-icon="mdi-close"></span>
        </span>
        <input type="time" name="{{ 'v%d%d' % (day, slot) }}" {{ 'value=%0.2d:%0.2d' % (hour, minute) if minutes <= 60 * 24 else '' }}>
    </div>
</div>