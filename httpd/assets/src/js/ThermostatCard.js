class ThermostatCard {

    constructor(card) {

        this.card = card;
        this.addr = this.card.dataset.addr;
        this.name = this.card.dataset.name;
        if (this.addr !== '') {
            this.initElements()
                .initData()
                .initHandler()
                .addObserver()
        }
    }

    initElements() {
        this.wanted = this.card.querySelector('[data-item="wanted"] input');

        return this;
    }

    initData() {
        this.data = {
            wanted: this.wanted.value
        }
        return this;
    }

    initHandler() {
        this.handleWanted = this.wantedHandler.bind(this);
        return this;
    }

    addObserver() {

        if (this.wanted) {
            this.wanted.addEventListener('pointerup', this.handleWanted);
        }

        return this;
    }

    async wantedHandler() {
        if ("undefined" !== typeof this.wantedTimeout) {
            clearTimeout(this.wantedTimeout)
        }
        this.wantedTimeout = setTimeout(() => {
            try {
                if (this.data.wanted !== this.wanted.value) {
                    let response = axios.post('http://localhost:3000/temp', {
                        addr: this.addr.toString(),
                        temp: this.wanted.value.toString()
                    })
                    console.info('Temperature of \'%s\' set to %s °C', this.name, this.wanted.value);
                }
            } catch (e) {
                console.error(e)
            } finally {
                delete this.wantedTimeout
            }
        }, 1000)
    }
}

export {ThermostatCard}