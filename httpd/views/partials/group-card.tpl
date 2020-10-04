<div class="group--card">
    <span class="group--name">{{ group.name }}</span>
    <ul class="group--devices">
        <li class="group--devices-header">
          <span class="label">Devices</span>
          <span class="iconify" data-icon="mdi-plus-outline"></span>
        </li>
        % for device in group.devices:
        % include('./partials/group-card/device')
        % end
    </ul>
</div>
