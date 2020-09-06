import Iconify from '@iconify/iconify';

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.thermostat-card--item[data-item="wanted"] input').forEach(field => {
        field.addEventListener('input', function() {
            let precision = this.value >= 10 ? 4 : 3
            this.closest('.thermostat-card--item')
                .querySelector('.value-display span').innerText = parseFloat(this.value)
                .toPrecision(precision).padStart(5, ' ')
        })
    });
});