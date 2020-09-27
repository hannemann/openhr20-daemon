class ThermostatsUpdater {

    constructor() {
        this.cards = {};
        this.ws = {};
        document.querySelectorAll('.thermostats .thermostat--card').forEach(c => {
            this.cards[c.dataset.addr] = c
        });
        this.interval = 30000;
        this.interval = 5000;

        if (Object.keys(this.cards).length > 0) {
            this.initWebsockets();
            this.initHandler()//.startInterval()
        }
    }

    initWebsockets() {
        for (let card of Object.values(this.cards)) {
            if (!this.ws.hasOwnProperty(card.dataset.ws)) {
                this.ws[card.dataset.ws] = new WebSocket(card.dataset.ws);
                this.ws[card.dataset.ws].onmessage = (e) => {
                    try {
                        let data = JSON.parse(e.data);
                        if ('stats' === data.type) {
                            let response = {
                                data : {
                                    [data.payload.addr]: {stats: data.payload}
                                }
                            }
                            this.updateHandler(response)
                        }
                    } catch (e) {

                    }
                }
            }
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
                let keys = k.split('-')

                let key = keys.shift();
                key += keys.map(k => k.charAt(0).toUpperCase() + k.slice(1)).join('');

                this.cards[addr].dataset[key] = data.stats[k];
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