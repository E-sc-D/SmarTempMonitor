document.addEventListener("DOMContentLoaded", () => {
    // Connect to the server using Socket.IO
    const socket = io();
    const value = document.getElementById("value");
    const avg = document.getElementById("avg");
    const max = document.getElementById("max");
    const min = document.getElementById("min");
    const tempLimit = 100;
    const valueBar = document.querySelector(".vertical-bars li:nth-child(4)");
    const avgBar = document.querySelector(".vertical-bars li:nth-child(3)");
    const maxBar = document.querySelector(".vertical-bars li:nth-child(1)");
    const minBar = document.querySelector(".vertical-bars li:nth-child(2)");

    window.addEventListener('beforeunload', () => {
        socket.disconnect();
    });

    timeLabels = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00"];  // Time labels
    temperatures = [20, 22, 24, 21, 23, 25];  // Corresponding temperatures

    // Set up the chart
    const ctx = document.getElementById('temperatureChart').getContext('2d');
    const temperatureChart = new Chart(ctx, {
        type: 'line',  // Line chart
        data: {
            labels: timeLabels,  // Time labels
            datasets: [{
                label: 'Temperature (°C)',  // Label for the data
                data: temperatures,  // Temperature data
                borderColor: 'rgba(75, 192, 192, 1)',  // Line color
                backgroundColor: 'rgba(75, 192, 192, 0.2)',  // Fill under the line (optional)
                fill: true,  // Optional: fill under the line
                tension: 0.1  // Smoothness of the line
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time'  // X-axis label (time)
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Temperature (°C)'  // Y-axis label (temperature)
                    },
                    min: 0, 
                    max: 100,
                    stepSize: 5 // Optional: set the minimum value for the y-axis
                }
            }
        }
    });

    function sendData() {
        const dataToSend = {
            message: "Hello from the client!",
            number: Math.floor(Math.random() * 100) // Example of sending a random number
        };
        socket.emit("client_data", dataToSend);
        console.log("Data sent to server:", dataToSend);
    }

    function getTempPercentage(currentTemp) {
        // Calculate the percentage of the current temperature relative to the max temperature
        let percentage = (currentTemp / tempLimit) * 100;
    
        // Cap the percentage at 100%
        if (percentage > 100) {
            percentage = 100;
        }
    
        // Return the value as a string to be used in CSS (e.g., for width, background, etc.)
        return `${percentage}%`;
    }

    function getCurrentTime() {
        const now = new Date();  // Get the current date and time
        let minutes = now.getMinutes();  // Get the minutes
        let seconds = now.getSeconds();  // Get the seconds
    
        // Format the time to always display two digits (e.g., "09:05" instead of "9:5")
        minutes = minutes < 10 ? '0' + minutes : minutes;
        seconds = seconds < 10 ? '0' + seconds : seconds;
    
        // Return the formatted time as "minutes:seconds"
        return `${minutes}:${seconds}`;
    }

    // Listen for data from the server
    socket.on("temp_reading", (data) => {
        
        value.textContent = data.temp;
        valueBar.style.height = getTempPercentage(data.temp)
        avg.textContent = `${ Math.round((temperatures.reduce((acc, curr) => acc + curr, 0))/temperatures.length)}`;
        avgBar.style.height = getTempPercentage(avg.textContent);
        max.textContent = Math.max(...temperatures);
        maxBar.style.height = getTempPercentage(max.textContent);
        min.textContent = Math.min(...temperatures);
        minBar.style.height = getTempPercentage(min.textContent);
        timeLabels.push(getCurrentTime());
        temperatures.push(data.temp);
    
        if (temperatures.length > 14) {
            temperatures.shift();  // Remove the first element
            timeLabels.shift();    // Remove the first time label
        }
    
        // Update the chart's data
        temperatureChart.data.labels = timeLabels;
        temperatureChart.data.datasets[0].data = temperatures;
    
        // Update the chart
        temperatureChart.update();
    });

    
});