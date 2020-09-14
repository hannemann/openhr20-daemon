
% type = 'daily_timers' if day == 0 else 'week_timers'
<div class="weekday--card" data-type="{{ type }}">
    <h3>{{ header[day] }}</h3>
    % for slot in range(8):
    % preset = timers[day][slot][0] if timers[day] is not None and timers[day][slot] is not '' else '0'
    % minutes = int(timers[day][slot][1:4], 16) if timers[day] is not None and timers[day][slot] is not '' else 24 * 60 + 1
    % hour = (minutes - (minutes % 60)) / 60 if minutes <= 60 * 24 else 0
    % minute = minutes % 60 if minutes <= 60 * 24 else 0

    %include('./partials/timer-slot')
    % end
</div>