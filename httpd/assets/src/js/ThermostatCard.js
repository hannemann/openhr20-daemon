class ThermostatCard {

    constructor(card) {

        this.card = card;
        this.addr = this.card.dataset.addr;
        this.name = this.card.dataset.name;
        if (this.addr !== '') {
            this.initElements()
                .initHandler()
                .addObserver()
        }
    }

    initElements() {
        this.wanted = this.card.querySelector('[data-item="wanted"] input');

        return this;
    }

    initHandler() {
        this.handleWanted = this.wantedHandler.bind(this);
        this.handleWantedInout = this.wantedInputHandler.bind(this);
        this.handleAttributeMutation = this.attributeMutationHandler.bind(this);
        return this;
    }

    addObserver() {
        this.observer = new MutationObserver(mutations => mutations.forEach(this.handleAttributeMutation));
        this.observer.observe(this.card, { attributes: true });

        if (this.wanted) {
            this.wanted.addEventListener('pointerdown', () => this.card.dataset.preventupdate = 'true');
            this.wanted.addEventListener('pointerup', this.handleWanted);
            this.wanted.addEventListener('input', this.handleWantedInout)
        }

        return this;
    }

    attributeMutationHandler(mutation) {
            let attribute = mutation.attributeName.replace('data-', '');
            let value = this.card.dataset[attribute];

            if (['wanted', 'synced'].indexOf(attribute) < -1) {
                this.card.querySelector(`[data-item="${attribute}"] .value-display span`).innerText = value;
            }

            if (!this.card.dataset.preventupdate) {
                if ('wanted' === attribute && this.card.dataset.synced === 'true') {
                    this.wanted.value = value;
                    this.wanted.dispatchEvent(new Event("input"));
                }
            }

            if ('synced' === attribute) {
                this.wanted.disabled = value === 'false'
            }
    }

    wantedHandler() {
        if ("undefined" !== typeof this.wantedTimeout) {
            clearTimeout(this.wantedTimeout)
        }
        this.wantedTimeout = setTimeout(async () => {
            try {
                delete this.card.dataset.preventupdate;
                if (this.card.dataset.wanted !== this.wanted.value) {
                    this.card.dataset.synced = 'false';
                    await axios.post(`${location.origin}/temp`, {
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

    wantedInputHandler() {

        let precision = this.wanted.value >= 10 ? 3 : 2
        this.wanted.closest('.thermostat-card--item')
            .querySelector('.value-display span').innerText = parseFloat(this.wanted.value)
            .toPrecision(precision).padStart(5, ' ')
    }
}

export {ThermostatCard}