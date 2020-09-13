class Settings {

    constructor() {
        if (document.querySelector('.thermostat-settings')) {
            this.run()
        }
    }

    run() {

        this.settings = Array.from(document.querySelectorAll('.thermostat-settings .setting input'));
        this.settings.forEach(s => {
            s.addEventListener('input', function() {
                let parent = this.closest('.field');
                parent.querySelector('span').dataset.int = this.value;
                parent.querySelector('span').dataset.hex = `(0x${this.valueAsNumber.toString(16).padStart(2, '0')})`
            })
        })

        document.querySelector('.thermostat-settings button[data-action="save"]').addEventListener('click', async () => {

            let data = {};

            this.settings.map(s => {
                data[s.name] = s.valueAsNumber.toString(16).padStart(2, '0')
            })
            await axios.post(`${location.origin}/settings/${location.pathname.split('/').pop()}`, data);
            location.href = location.origin;
        })

        document.querySelector('.thermostat-settings button[data-action="reboot"]').addEventListener('click', async () => {

            await axios.post(`${location.origin}/reboot/${location.pathname.split('/').pop()}`);
            location.href = location.origin;
        })

        document.querySelector('.thermostat-settings button[data-action="refresh"]').addEventListener('click', async () => {

            await axios.post(`${location.origin}/request_settings/${location.pathname.split('/').pop()}`);
            location.href = location.origin;
        })

    }

}

export {Settings}