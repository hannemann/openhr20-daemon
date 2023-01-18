import { ThermostatCard } from "./js/ThermostatCard.js";
import { ThermostatsUpdater } from "./js/ThermostatsUpdater.js";
import { Settings } from "./js/Settings.js";
import { Timers } from "./js/Timers.js";
import { DeviceManager } from "./js/DeviceManager.js";

document.addEventListener("DOMContentLoaded", () => {
  new ThermostatsUpdater();
  new Settings();
  new Timers();
  new DeviceManager();
  document
    .querySelectorAll(".thermostats .thermostat--card")
    .forEach((c) => new ThermostatCard(c));
});
