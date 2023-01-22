class Timers {
  constructor() {
    if (document.querySelector(".thermostat-timers")) {
      this.run();
    }
  }

  run() {
    const proto = location.protocol.replace("http", "ws");
    const port = document.querySelector(":root head base").dataset.wsPort;
    const url = `${proto}//${location.hostname}:${port}`;
    const addr = document.querySelector(".thermostat-timers").dataset.addr;
    console.info("Init websocket connection to %s", url);
    const connection = new WebSocket(url);
    document
      .querySelectorAll('.timer-slot input[type="range"]')
      .forEach((i) => {
        i.addEventListener("input", () => {
          let parent = i.closest(".timer-slot--preset");
          parent.querySelector("output").value = Array.from(
            parent.querySelector("datalist").options
          ).find((o) => {
            return o.value === i.value;
          }).label;
        });
      });

    document.querySelectorAll(".timer-slot span.timer-delete").forEach((i) => {
      i.addEventListener("pointerup", () => {
        i.parentNode.querySelector('input[type="time"]').value = "";
      });
    });

    document.querySelectorAll(".timer-mode--card input").forEach((i) => {
      i.addEventListener("input", () => {
        document.querySelector(".thermostat-timers").dataset.mode = i.value;
      });
    });

    document
      .querySelector('.thermostat-timers button[data-action="save"]')
      .addEventListener("click", () => {
        let data = {
          timers: {},
          mode: document.querySelector('input[name="G22"]:checked').value,
        };

        document.querySelectorAll(".timer-slot").forEach((s) => {
          let index = s.querySelector("input").name.substr(1);
          data.timers[index] = [
            s.querySelector("input").value,
            (
              s
                .querySelector('input[type="time"]')
                .value.split(":")
                .reverse()
                .map((v, k) => (k ? 60 : 1) * parseInt(v, 10))
                .reduce((a, c) => a + c) || parseInt("fff", 16)
            ).toString(16),
          ].join("");
        });
        connection.send(
          JSON.stringify({
            type: "save_timers",
            addr: parseInt(addr),
            timers: data.timers,
            mode: data.mode,
          })
        );
        location.href = document.baseURI;
      });

    document
      .querySelector('.thermostat-timers button[data-action="refresh"]')
      .addEventListener("click", () => {
        connection.send(
          JSON.stringify({
            type: "request_timers",
            addr: parseInt(addr),
          })
        );
        location.href = document.baseURI;
      });
  }
}

export { Timers };
