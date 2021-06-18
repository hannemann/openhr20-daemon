import {errorIconMap} from './ThermostatCard.js';

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
            this.initHandler()
                .initWebsockets()
                .addObserver()
            ;
        }
    }

    initHandler() {
        this.handleVisibility = this.visibilityHandler.bind(this);
        this.handleSocketOpen = this.socketOpenHandler.bind(this)

        return this;
    }

    initWebsockets() {
        console.info('Init websocket connections');
        for (let card of Object.values(this.cards)) {
            if (!this.ws.hasOwnProperty(card.dataset.ws)) {
                this.ws[card.dataset.ws] = new WebSocket(card.dataset.ws);
                this.ws[card.dataset.ws].onmessage = (e) => {
                    try {
                        let data = JSON.parse(e.data);
                        if ('stats' === data.type) {
                            this.updateHandler(data.payload)
                        }
                    } catch (e) {

                    }
                }
                this.ws[card.dataset.ws].addEventListener('open', this.handleSocketOpen)
            }
        }
        return this;
    }

    closeWebsockets() {
        console.info('Closing websocket connections');
        Object.keys(this.ws).forEach(s => {
            this.ws[s].removeEventListener('open', this.handleSocketOpen)
            this.ws[s].close()
            delete this.ws[s]
        })
        return this;
    }

    addObserver() {

        document.addEventListener('visibilitychange', this.handleVisibility)
        return this;
    }

    socketOpenHandler(e) {
        e.currentTarget.send(JSON.stringify({
            type: 'update_stats'
        }))
    }

    updateHandler(stats) {
        Object.keys(stats).forEach(k => {
            let keys = k.split('-'), value

            let key = keys.shift();
            key += keys.map(k => k.charAt(0).toUpperCase() + k.slice(1)).join('');

            if ('error' === key) {
                let values = [];
                Object.keys(errorIconMap).forEach(e => {
                    if ((stats[k] & e) === parseInt(e, 10)) {
                        values.push(e);
                    }
                })
                value = values.join('|') + '|';
            } else {
                value = stats[k];
            }

            this.cards[stats.addr].dataset[key] = value;
        })
    }

    visibilityHandler() {
        if (document.hidden) {
            this.closeWebsockets()
        } else {
            this.initWebsockets()
        }
    }
}

export {ThermostatsUpdater}