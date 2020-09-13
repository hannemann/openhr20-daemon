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
        this.mode = this.card.querySelector('[data-item="mode"] .mode-button');
        this.update = this.card.querySelector('h3 .update-button');

        return this;
    }

    initHandler() {
        this.handleUpdate = this.updateHandler.bind(this);
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
        if (this.update) {
            this.update.addEventListener('pointerup', this.handleUpdate);
        }

        return this;
    }

    attributeMutationHandler(mutation) {
        let attribute = mutation.attributeName.replace('data-', ''),
            value = this.card.dataset[attribute],
            selector = `[data-item="${attribute}"] .value-display span`
        ;

        if (['wanted', 'synced', 'time'].indexOf(attribute) < -1) {
            this.card.querySelector(selector).innerText = value;
        }

        if (!this.card.dataset.preventupdate) {
            if ('wanted' === attribute && this.card.dataset.synced === 'true') {
                if (this.wanted) {
                    this.wanted.value = value;
                    this.wanted.dispatchEvent(new Event("input"));
                }
            }
        }

        if ('synced' === attribute) {
            if (this.wanted) {
                this.wanted.disabled = value === 'false'
            }
        }

        if ('time' === attribute) {
            let d = new Date(value * 1000);
            this.card.querySelector('h3 [data-item="time"]').innerText = `${d.getDate().toString(10).padStart(2, '0')}.`
                + `${(d.getMonth() + 1).toString(10).padStart(2, '0')}.`
                + `${d.getFullYear().toString(10)} `
                + `${d.getHours().toString(10).padStart(2, '0')}:`
                + `${d.getMinutes().toString(10).padStart(2, '0')}:`
                + `${d.getSeconds().toString(10).padStart(2, '0')}`
            ;
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

    async updateHandler() {
        try {
            let data = {
                addr: this.addr.toString(),
            }
            this.card.dataset.synced = 'false';
            await axios.post(`${location.origin}/update`, data)
            console.info('Update of \'%s\' requested', this.name);
        } catch (e) {
            console.error(e)
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