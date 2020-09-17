import Iconify from '@iconify/iconify';
import axios from 'axios';
import {ThermostatCard} from "./js/ThermostatCard";
import {ThermostatsUpdater} from "./js/ThermostatsUpdater";
import {Settings} from "./js/Settings";
import {Timers} from "./js/Timers";

window.axios = axios;

document.addEventListener('DOMContentLoaded', () => {

    new ThermostatsUpdater();
    new Settings();
    new Timers();
    document.querySelectorAll('.thermostats .thermostat--card').forEach(c => new ThermostatCard(c));
});