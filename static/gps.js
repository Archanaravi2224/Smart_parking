const map = L.map('map'); // Initialize the map without setting a static view

// Load OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

let userMarker; // Initialize user marker

// Function to reverse geocode the latitude and longitude
function reverseGeocode(lat, lng) {
    fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`)
        .then(response => response.json())
        .then(data => {
            console.log("Address:", data.display_name); // Log the address
            // You can display the address in your UI if needed
        })
        .catch(error => console.error('Error in reverse geocoding:', error));
}

// Function to update GPS
function updateGPS() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const lat = position.coords.latitude; // Get latitude
            const lng = position.coords.longitude; // Get longitude
            const timestamp = new Date().toISOString(); // Get the current timestamp

            // Check if the userMarker exists
            if (userMarker) {
                userMarker.setLatLng([lat, lng]); // Update marker position
            } else {
                userMarker = L.marker([lat, lng]).addTo(map); // Create a new marker if it doesn't exist
                map.setView([lat, lng], 13); // Center the map on the user's current location for the first time
            }

            // Send GPS data to the backend
            fetch('/gps/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ latitude: lat, longitude: lng, timestamp: timestamp }) // Sending data
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                console.log("GPS data updated successfully"); // Log success
            })
            .catch(error => console.error('Error sending GPS data:', error)); // Log errors

            // Call reverse geocoding to get the address
            reverseGeocode(lat, lng); // Call reverse geocoding
        }, error => {
            console.error('Error getting location:', error); // Handle location errors
        }, {
            enableHighAccuracy: true, // Request high accuracy
            timeout: 5000,
            maximumAge: 0 // No cached position
        });
    } else {
        console.error('Geolocation is not supported by this browser.'); // Handle unsupported browsers
    }
}

// Call updateGPS every 5 seconds
setInterval(updateGPS, 5000);
