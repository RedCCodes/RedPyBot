document.addEventListener('DOMContentLoaded', (event) => {
    const volumeSlider = document.getElementById('volume');
    const volumeValue = document.getElementById('volume-value');

    if (volumeSlider && volumeValue) {
        volumeSlider.addEventListener('input', () => {
            volumeValue.textContent = volumeSlider.value;
        });
    }
});
