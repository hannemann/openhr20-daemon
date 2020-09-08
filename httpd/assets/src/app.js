import Iconify from '@iconify/iconify';
import axios from 'axios';
import {ThermostatCard} from "./js/ThermostatCard";

window.axios = axios;

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.thermostat-card--item[data-item="wanted"] input').forEach(field => {
        field.addEventListener('input', function() {
            let precision = this.value >= 10 ? 4 : 3
            this.closest('.thermostat-card--item')
                .querySelector('.value-display span').innerText = parseFloat(this.value)
                .toPrecision(precision).padStart(5, ' ')
        })
    });

    document.querySelectorAll('.thermostat-card').forEach(c => new ThermostatCard(c));
});