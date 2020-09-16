class ThermostatsUpdater {

    constructor() {
        this.cards = {};
        document.querySelectorAll('.thermostat-card').forEach(c => {
            this.cards[c.dataset.addr] = c
        });
        this.interval = 30000;
        this.interval = 5000;

        if (Object.keys(this.cards).length > 0) {
            this.initHandler().startInterval()
        }
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
            let cancelTimeout = null, source = axios.CancelToken.source();
            cancelTimeout = setTimeout(() => source.cancel('Stats request cancelled after 2s'), 2000)
            try {
                let response = await axios.get(`${location.origin}/stats`, {cancelToken: source.token});
                this.handleUpdate(response);
            } catch(e) {
                if (axios.isCancel(e)) {
                    console.error(e.message)
                } else {
                    console.error(e)
                }
            } finally {
                clearTimeout(cancelTimeout)
            }
        }, this.interval)
    }

}

export {ThermostatsUpdater}