document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('sensorChart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Temperature (°C)',
                data: [],
                borderColor: 'rgb(13, 110, 253)',
                tension: 0.1
            }, {
                label: 'Humidity (%)',
                data: [],
                borderColor: 'rgb(25, 135, 84)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    function updateDashboard() {
        fetch('/data')
            .then(response => response.json())
            .then(data => {
                document.getElementById('temperature').textContent = 
                    data.temperature !== null ? `${data.temperature.toFixed(1)} °C` : '-- °C';
                document.getElementById('humidity').textContent = 
                    data.humidity !== null ? `${data.humidity.toFixed(1)} %` : '-- %';
                document.getElementById('co2').textContent = 
                    data.co2 !== null ? `${data.co2} ppm` : '-- ppm';
                document.getElementById('forecast').textContent =
                    data.forecast !== null ? `${data.forecast.toFixed(1)} ppm` : '-- ppm';
                document.getElementById('air-quality').textContent = 
                    data.air_quality || '--';
                
                // Show anomaly warning if detected
                if (data.anomaly) {
                    document.getElementById('anomaly').textContent = '⚠️ Anomaly Detected';
                } else {
                    document.getElementById('anomaly').textContent = '';
                }

                // Update chart
                if (data.temperature !== null && data.humidity !== null) {
                    const time = new Date().toLocaleTimeString();
                    chart.data.labels.push(time);
                    chart.data.datasets[0].data.push(data.temperature);
                    chart.data.datasets[1].data.push(data.humidity);
                
                    // Keep only last 15 data points
                    if (chart.data.labels.length > 15) {
                        chart.data.labels.shift();
                        chart.data.datasets.forEach(dataset => dataset.data.shift());
                    }
                    chart.update();
                }
            });
    }

    // Update every 3 seconds
    setInterval(updateDashboard, 7000);
    updateDashboard(); // Initial call
});