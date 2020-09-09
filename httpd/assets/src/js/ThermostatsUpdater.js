class ThermostatsUpdater {

    constructor() {
        this.cards = {};
        document.querySelectorAll('.thermostat-card').forEach(c => {
            this.cards[c.dataset.addr] = {
                wanted: c.querySelector('[data-item="wanted"]'),
                real: c.querySelector('[data-item="real"]'),
                valve: c.querySelector('[data-item="valve"]'),
                battery: c.querySelector('[data-item="battery"]'),
                synced: c.querySelector('[data-item="synced"]'),
            }
        });
        this.interval = 30000;
        this.interval = 5000;

        this.initHandler().startInterval()
    }

    initHandler() {
        this.handleUpdate = this.updateHandler.bind(this)

        return this;
    }

    updateHandler(response) {

        Object.keys(response.data).forEach(addr => {
            if ('undefined' !== typeof response.data[addr].stats.wanted) {
                this.updateWanted(addr, response.data[addr].stats.wanted)
            }
            if ('undefined' !== typeof response.data[addr].stats.real) {
                this.updateReal(addr, response.data[addr].stats.real)
            }
            if ('undefined' !== typeof response.data[addr].stats.valve) {
                this.updateValve(addr, response.data[addr].stats.valve)
            }
            if ('undefined' !== typeof response.data[addr].stats.battery) {
                this.updateBattery(addr, response.data[addr].stats.battery)
            }
            if ('undefined' !== typeof response.data[addr].stats.synced) {
                this.updateSynced(addr, response.data[addr].stats.synced)
            }
        })
    }

    startInterval() {
        setInterval(async () => {
            try {
                let response = await axios.get(`${location.origin}/stats`);
                this.handleUpdate(response);
            } catch(e) {
                console.error(e)
            }
        }, this.interval)
    }

    updateWanted(addr, value) {
        let input = this.cards[addr].wanted.querySelector('input');
        input.value = value;
        input.dispatchEvent(new Event("input"));
    }

    updateReal(addr, value) {
        this.cards[addr].real.querySelector('.value-display span').innerText = value;
    }

    updateValve(addr, value) {
        this.cards[addr].valve.querySelector('.value-display span').innerText = value;
    }

    updateBattery(addr, value) {
        this.cards[addr].battery.querySelector('.value-display span').innerText = value;
    }

    updateSynced(addr, value) {
        let iconSynced = this.cards[addr].synced.querySelector('.value-display span.synced'),
            iconNotSynced = this.cards[addr].synced.querySelector('.value-display span.not-synced');

        iconSynced.classList.toggle('hidden', !value);
        iconNotSynced.classList.toggle('hidden', value);
    }

}

export {ThermostatsUpdater}