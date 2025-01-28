document.addEventListener("DOMContentLoaded", () => {
    // Connect to the server using Socket.IO
    const socket = io();

    // Function to send data to the server
    function sendData() {
        const dataToSend = {
            message: "Hello from the client!",
            number: Math.floor(Math.random() * 100) // Example of sending a random number
        };
        socket.emit("client_data", dataToSend);
        console.log("Data sent to server:", dataToSend);
    }

    // Listen for data from the server
    socket.on("server_response", (data) => {
        console.log("Data received from server:", data);
        document.getElementById("server-message").innerText = JSON.stringify(data);
    });
});