document.addEventListener('DOMContentLoaded', function() {

    const onboardButton = document.getElementById('new-device-btn');
    const plotButton = document.getElementById('plot-btn');
    const dropdown = document.getElementById('device-dropdown');

    if (onboardButton) {
        onboardButton.addEventListener('click', function() {
            window.open('/onboard', 'OnboardWindow', 'width=600,height=600,resizable=yes,scrollbars=yes');
        });
    }

    if (plotButton && dropdown) {
        plotButton.addEventListener('click', function() {
            const selected = dropdown.value || 'UCY-001';
            const url = `/plotdata/${selected}`;
            window.open(url, 'PlotWindow', 'width=800,height=600,resizable=yes,scrollbars=yes');
        });
    }

});
