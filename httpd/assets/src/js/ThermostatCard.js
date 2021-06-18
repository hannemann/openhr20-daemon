const errorIconMap = {
    4: "mdi-cog-refresh-outline",
    8: "mdi-cog-off-outline",
    16: "mdi-access-point-off",
    64: "mdi-battery-alert-variant-outline",
    128: "mdi-battery-off-outline"

};

class ThermostatCard {

    constructor(card) {

        this.card = card;
        this.addr = this.card.dataset.addr;
        this.name = this.card.dataset.name;
        this.cancelTimeout = null;
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
        this.loading = this.card.querySelector('span.loading');
        this.cancel = this.card.querySelector('span.loading .cancel');
        this.presets = this.card.querySelectorAll('[data-item="presets"] span.preset');

        return this;
    }

    initHandler() {
        this.handleUpdate = this.updateHandler.bind(this);
        this.handleWanted = this.tempHandler.bind(this);
        this.handleWantedDown = this.wantedDownHandler.bind(this);
        this.handleMode = this.modeHandler.bind(this);
        this.handleWantedInput = this.wantedInputHandler.bind(this);
        this.handleAttributeMutation = this.attributeMutationHandler.bind(this);
        this.handleCancel = this.cancelHandler.bind(this);
        return this;
    }

    addObserver() {
        this.observer = new MutationObserver(mutations => mutations.forEach(this.handleAttributeMutation));
        this.observer.observe(this.card, { attributes: true });

        if (this.wanted) {
            this.wanted.addEventListener('pointerdown', this.handleWantedDown);
            this.wanted.addEventListener('pointerup', this.handleWanted);
            this.wanted.addEventListener('input', this.handleWantedInput);
        }
        if (this.mode) {
            this.mode.addEventListener('pointerdown', () => this.card.dataset.preventupdate = 'true');
            this.mode.addEventListener('pointerup', this.handleMode);
        }
        if (this.update) {
            this.update.addEventListener('pointerup', this.handleUpdate);
        }

        this.presets.forEach(p => {
            p.addEventListener('pointerdown', () => {
                this.wanted.value = p.dataset.temperature;
                this.handleWanted();
            })
        })

        this.cancel.addEventListener('pointerup', this.handleCancel);

        return this;
    }

    attributeMutationHandler(mutation) {
        let attribute = mutation.attributeName.replace('data-', ''),
            value = this.card.dataset[attribute],
            selector = `[data-item="${attribute}"] .value-display span`
        ;

        if (['real', 'valve', 'battery'].indexOf(attribute) > -1) {
            let item = this.card.querySelector(selector);
            if (item) {
                item.innerText = value;
            }
        }

        if (!this.card.dataset.preventupdate) {
            if ('wanted' === attribute && this.card.dataset.synced === 'true') {
                if (this.wanted) {
                    this.wanted.value = value;
                    this.wanted.dispatchEvent(new Event("input"));
                }
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

        if ('pending-commands' === attribute) {
            this.loading.dataset.pendingCommands = this.card.dataset.pendingCommands;
        }
    }

    async tempHandler() {
        try {
            delete this.wanted.parentNode.dataset.active;
            if (this.card.dataset.wanted !== this.wanted.value) {
                this.card.dataset.synced = 'false';
                await this.post(`${location.origin}/temp/${this.addr}`, {
                    temp: this.wanted.value.toString()
                })
                console.info('Temperature of \'%s\' set to %s °C', this.name, this.wanted.value);
            }
        } catch (e) {
            console.error(axios.isCancel(e) ? e.message : e)
        } finally {
            delete this.card.dataset.preventupdate;
            clearTimeout(this.cancelTimeout)
        }
    }

    async modeHandler() {
        try {
            let data = {
                mode: this.card.dataset.mode === 'manu' ? 'auto' : 'manu'
            }
            this.card.dataset.synced = 'false';
            await this.post(`${location.origin}/mode/${this.addr}`, data)
            console.info('Mode of \'%s\' set to %s', this.name, data.mode);
        } catch (e) {
            console.error(axios.isCancel(e) ? e.message : e)
        } finally {
            delete this.card.dataset.preventupdate;
            clearTimeout(this.cancelTimeout)
        }
    }

    async updateHandler() {
        try {
            this.card.dataset.synced = 'false';
            await this.post(`${location.origin}/update/${this.addr}`)
            console.info('Update of \'%s\' requested', this.name);
        } catch (e) {
            console.error(axios.isCancel(e) ? e.message : e)
        } finally {
            clearTimeout(this.cancelTimeout)
        }
    }

    async cancelHandler() {
        try {
            await this.post(`${location.origin}/cancel/${this.addr}`)
            console.info('Cancel of all commands for device \'%s\' requested', this.name);
        } catch (e) {
            console.error(axios.isCancel(e) ? e.message : e)
        } finally {
            clearTimeout(this.cancelTimeout)
        }
    }

    post(url, data) {
        let source = axios.CancelToken.source();
        this.cancelTimeout = setTimeout(() => {
            source.cancel(`Request to ${url} cancelled after 2s`)
        }, 2000)
        return axios.post(url, data, {cancelToken: source.token})
    }

    wantedDownHandler() {
        this.card.dataset.preventupdate = 'true';
    }

    wantedInputHandler() {

        let precision = this.wanted.value >= 10 ? 3 : 2,
            value = parseFloat(this.wanted.value).toPrecision(precision).padStart(5, ' '),
            item = this.wanted.closest('.thermostat--card--item');

        item.querySelector('.value-display span').innerText = value;

        if (parseFloat(value) === parseFloat(this.card.dataset.wanted)) {
            item.querySelector('.value-display').dataset.isCurrent = 'true';
        } else {
            delete item.querySelector('.value-display').dataset.isCurrent;
        }

    }
}

export {errorIconMap, ThermostatCard}