class ThermostatsUpdater {

    constructor() {
        this.cards = {};
        document.querySelectorAll('.thermostat-card').forEach(c => {
            this.cards[c.dataset.addr] = c
        });
        this.interval = 30000;
        this.interval = 5000;

        this.initHandler().startInterval()
    }

    initHandler() {
        this.handleUpdate = this.updateHandler.bind(this)

        return this;
    }

    canUpdate(data, addr) {
        return "undefined" !== typeof this.cards[addr] &&
            !this.cards[addr].dataset.syncing &&
            data.stats.synced
    }

    updateHandler(response) {

        Object.keys(response.data).forEach(addr => {
            let data = response.data[addr];
            Object.keys(data.stats).forEach(k => {
                this.cards[addr].dataset[k] = data.stats[k];
            })
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

}

export {ThermostatsUpdater}