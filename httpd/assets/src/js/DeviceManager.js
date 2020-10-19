class DeviceManager {

    constructor() {
        this.el = document.querySelector('.device-manager')
        if (this.el) {
            this.initData()
                .initTemplates()
                .initUi();
        }
    }

    initData() {
        this.devices = JSON.parse(this.el.dataset.devices);
        this.groups = JSON.parse(this.el.dataset.groups);
        return this;
    }

    initTemplates() {
        let groupTemplate = document.querySelector('#group-template'),
            deviceTemplate = document.querySelector('#group-device-template'),
            ungroupedTemplate =document.querySelector('#ungrouped-device-template');
        this.group = groupTemplate.content.querySelector('.group--card');
        this.device = deviceTemplate.content.querySelector('.group--device');
        this.ungrouped = ungroupedTemplate.content.querySelector('div')
        return this;
    }

    initUi() {
        this.groups.forEach(this.createGroup.bind(this));
        this.devices.filter(d => d.group == null)
            .forEach(this.createUngroupedDevice.bind(this));
    }

    createGroup(groupDef) {
        this.group.querySelector('.group--name').textContent = groupDef.name;
        let group = document.importNode(this.group, true);
        groupDef.devices.forEach(d => {
            this.device.querySelector('.label')
                .textContent = this.devices.find(f => f.addr == d).name;
            let device = document.importNode(this.device, true);
            group.querySelector('.group--devices').appendChild(device);
        });
        this.el.querySelector('.groups').appendChild(group);
    }

    createUngroupedDevice(device) {
        this.ungrouped.textContent = device.name;
        this.el.querySelector('.ungrouped-devices').appendChild(
            document.importNode(this.ungrouped, true)
        )
    }

}

export {DeviceManager}
