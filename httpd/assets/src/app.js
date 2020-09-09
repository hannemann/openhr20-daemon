import Iconify from '@iconify/iconify';
import axios from 'axios';
import {ThermostatCard} from "./js/ThermostatCard";
import {ThermostatsUpdater} from "./js/ThermostatsUpdater";

window.axios = axios;

document.addEventListener('DOMContentLoaded', () => {

    new ThermostatsUpdater();
    document.querySelectorAll('.thermostat-card').forEach(c => new ThermostatCard(c));
});