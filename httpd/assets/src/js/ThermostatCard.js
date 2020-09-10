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
        this.mode = this.card.querySelector('[data-item="mode"]');

        return this;
    }

    initHandler() {
        this.handleWanted = this.tempHandler.bind(this);
        this.handleMode = this.modeHandler.bind(this);
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
        if (this.mode) {
            this.mode.addEventListener('pointerdown', () => this.card.dataset.preventupdate = 'true');
            this.mode.addEventListener('pointerup', this.handleMode);
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

    async tempHandler() {
        try {
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
            delete this.card.dataset.preventupdate;
        }
    }

    async modeHandler() {
        try {
            let data = {
                addr: this.addr.toString(),
                mode: this.card.dataset.mode === 'manu' ? 'auto' : 'manu'
            }
            this.card.dataset.synced = 'false';
            await axios.post(`${location.origin}/mode`, data)
            console.info('Mode of \'%s\' set to %s', this.name, data.mode);
        } catch (e) {
            console.error(e)
        } finally {
            delete this.card.dataset.preventupdate;
        }
    }

    wantedInputHandler() {

        let precision = this.wanted.value >= 10 ? 3 : 2
        this.wanted.closest('.thermostat-card--item')
            .querySelector('.value-display span').innerText = parseFloat(this.wanted.value)
            .toPrecision(precision).padStart(5, ' ')
    }
}

export {ThermostatCard}