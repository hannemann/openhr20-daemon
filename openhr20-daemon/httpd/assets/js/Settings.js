import { ws } from "./ThermostatsUpdater.js";

class Settings {
  constructor() {
    if (document.querySelector(".thermostat-settings")) {
      this.run();
    }
  }

  run() {
    const proto = location.protocol.replace("http", "ws");
    const port = document.querySelector(":root head base").dataset.wsPort;
    const url = `${proto}//${location.hostname}:${port}`;
    const addr = document.querySelector(".thermostat-settings").dataset.addr;
    console.info("Init websocket connection to %s", url);
    const connection = new WebSocket(url);
    this.settings = Array.from(
      document.querySelectorAll(".thermostat-settings .setting--card input")
    );
    this.settings.forEach((s) => {
      s.addEventListener("input", function () {
        let parent = this.closest(".field");
        parent.querySelector("span").dataset.int = this.value;
        parent.querySelector("span").dataset.hex = `(0x${this.valueAsNumber
          .toString(16)
          .padStart(2, "0")})`;
      });
    });

    document
      .querySelector('.thermostat-settings button[data-action="save"]')
      .addEventListener("click", () => {
        let settings = {};
        this.settings.map((s) => {
          settings[s.name] = s.valueAsNumber.toString(16).padStart(2, "0");
        });
        connection.send(
          JSON.stringify({
            type: "save_settings",
            addr: parseInt(addr),
            settings,
          })
        );
        location.href = document.baseURI;
      });

    document
      .querySelector('.thermostat-settings button[data-action="reboot"]')
      .addEventListener("click", () => {
        connection.send(
          JSON.stringify({
            type: "reboot",
            addr: parseInt(addr),
          })
        );
        location.href = document.baseURI;
      });

    document
      .querySelector('.thermostat-settings button[data-action="refresh"]')
      .addEventListener("click", () => {
        connection.send(
          JSON.stringify({
            type: "request_settings",
            addr: parseInt(addr),
          })
        );
        location.href = document.baseURI;
      });
  }
}

export { Settings };
