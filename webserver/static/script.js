let socket; 
let value;
let avg ;
let max ;
let min ;
let tempLimit; 
let valueBar ;
let avgBar; 
let maxBar ;
let minBar ;
let circleToggle; 
let circleIndicator; 
let circleInput ;


document.addEventListener("DOMContentLoaded", () => {
    // Connect to the server using Socket.IO
    socket = io();
    value = document.getElementById("value");
    avg = document.getElementById("avg");
    max = document.getElementById("max");
    min = document.getElementById("min");
    tempLimit = 100;
    valueBar = document.querySelector(".vertical-bars li:nth-child(4)");
    avgBar = document.querySelector(".vertical-bars li:nth-child(3)");
    maxBar = document.querySelector(".vertical-bars li:nth-child(1)");
    minBar = document.querySelector(".vertical-bars li:nth-child(2)");
    circleToggle = document.querySelector(".circle button");
    circleIndicator = document.querySelector(".circle");
    circleInput = document.querySelector(".circle input");
    resetButton = document.querySelector(".subsection button");

    circleInput.addEventListener("change", function (event) {
            socket.emit("client_data", {"window": event.target.value});
            circleIndicator.style.background =  `conic-gradient(#2d8ff9 0% ${event.target.value}%, lightgray 0% 100%)`;

        });
      
    resetButton.addEventListener("click",() =>{
            socket.emit("reset",{"btn": 0});
    });

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
            animation: false,
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
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
                    max: 70,
                    stepSize: 5 // Optional: set the minimum value for the y-axis
                }
            }
        }
    });

    
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

    function changeButtonState(status) {
    
        // Remove any existing state classes
        resetButton.classList.remove("state-0", "state-1", "state-2", "state-3");
    
        // Add the new state class
        resetButton.classList.add(`state-${status}`);
    }

    // Listen for data from the server
    socket.on("temp_reading", (data) => {
        
        value.textContent = data.temp;
        valueBar.style.height = getTempPercentage(data.temp)
        let media = 0;
        for (let i = 0; i < temperatures.length; i++) {
            media += Math.round(temperatures[i]);
        }
        avg.textContent = `${ (media/temperatures.length).toFixed(2) }`;
        avgBar.style.height = getTempPercentage(avg.textContent);
        max.textContent = Math.max(...temperatures);
        maxBar.style.height = getTempPercentage(max.textContent);
        min.textContent = Math.min(...temperatures);
        minBar.style.height = getTempPercentage(min.textContent);
        changeButtonState(data.status);
        if(circleToggle.getAttribute("switchstate") === "off"){
            circleInput.value = data.window;
            circleIndicator.style.background =  `conic-gradient(#2d8ff9 0% ${data.window}%, lightgray 0% 100%)`;
        } 
          
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

function toggleManual(){
    if(circleToggle.getAttribute("switchstate") === "on"){
        circleToggle.setAttribute("switchstate","off");
        circleInput.disabled = true;
    }else{
        circleToggle.setAttribute("switchstate","on");
        circleInput.disabled = false;
    }
}