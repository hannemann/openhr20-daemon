class Timers {

    constructor() {
        if (document.querySelector('.thermostat-timers')) {
            this.run();
        }
    }

    run() {
        document.querySelectorAll('.timer-slot input[type="range"]').forEach(i => {
            i.addEventListener('input', () => {
                let parent = i.closest('.timer-slot--preset');
                parent.querySelector('output')
                    .value = Array.from(parent.querySelector('datalist').options).find(o => {
                    return o.value === i.value;
                }).label
            })
        })

        document.querySelectorAll('.timer-slot span.timer-delete').forEach(i => {
            i.addEventListener('pointerup', () => {
                i.parentNode.querySelector('input[type="time"]').value = '';
            })
        })
        
        document.querySelectorAll('.timer-mode--card input').forEach(i => {
            i.addEventListener('input', () => {
                document.querySelector('.thermostat-timers').dataset.mode = i.value;
            })
        })

        document.querySelector('.thermostat-timers button[data-action="save"]').addEventListener('click', async () => {

            let data = {};

            document.querySelectorAll('.timer-slot').forEach(s => {
                let index = s.querySelector('input').name.substr(1);
                data[index] = [
                    s.querySelector('input').value,
                    (s.querySelector('input[type="time"]').value.split(':').reverse()
                        .map((v, k) => (k ? 60 : 1) * parseInt(v, 10))
                        .reduce((a, c) => a + c) || parseInt('fff', 16)).toString(16)
                ].join('');
            })

            await axios.post(`${location.origin}/set_timers/${location.pathname.split('/').pop()}`, data);
            location.href = location.origin;
        })

        document.querySelector('.thermostat-timers button[data-action="refresh"]').addEventListener('click', async () => {

            await axios.post(`${location.origin}/request_timers/${location.pathname.split('/').pop()}`);
            location.href = location.origin;
        })
    }

}

export {Timers}