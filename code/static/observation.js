document.addEventListener("DOMContentLoaded", function () {
    loadDropdown("user", "/api/users");
    loadDropdown("species", "/api/species");

    document.getElementById("obs-form").addEventListener("submit", async function (event) {
        event.preventDefault();

        const latitude = parseFloat(document.getElementById("latitude").value);
        const longitude = parseFloat(document.getElementById("longitude").value);
        const placeName = document.getElementById("place_name").value.trim() || "Unnamed Place";

        console.log(`Checking place: ${placeName} at (${latitude}, ${longitude})`);

        const pid = await getOrCreatePlace(latitude, longitude, placeName);

        if (!pid) {
            alert("Error: Could not create or find a place.");
            return;
        }

        const observationData = {
            user_id: document.getElementById("user").value,
            species: document.getElementById("species").value,
            timestamp: document.getElementById("timestamp").value,
            behavior: document.getElementById("behavior").value,
            description: document.getElementById("description").value,
            pid: pid
        };

        console.log("Sending Observation Data:", observationData);

        try {
            const response = await fetch("/api/observations", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(observationData)
            });

            const result = await response.json();
            console.log("Observation Response:", result);
            alert(result.message || result.error);
        } catch (error) {
            console.error("Error submitting observation:", error);
            alert("Error submitting observation.");
        }
    });
});

async function getOrCreatePlace(latitude, longitude, placeName) {
    if (!placeName) placeName = "Unnamed Place";

    try {
        let response = await fetch(`/api/places/search?latitude=${latitude}&longitude=${longitude}&place_name=${encodeURIComponent(placeName)}`);
        let data = await response.json();

        if (data.exists && data.pid) {
            return data.pid;
        }
        const placeData = {
            place_name: placeName,
            latitude: latitude,
            longitude: longitude
        };

        let newPlaceResponse = await fetch("/api/places", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(placeData)
        });

        let newPlaceData = await newPlaceResponse.json();
        console.log("Place Creation Response:", newPlaceData);

        if (newPlaceData.pid) {
            console.log("Place created with pid:", newPlaceData.pid);
            return newPlaceData.pid;
        }

        console.error(" Error: Place was created but no pid returned.");
        return null;

    } catch (error) {
        console.error("Error finding or creating place:", error);
        return null;
    }
}



function loadDropdown(elementId, apiUrl) {
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            console.log(`Dropdown Data for ${elementId}:`, data);
            const dropdown = document.getElementById(elementId);
            dropdown.innerHTML = '<option value="">Select an option</option>';

            data.forEach(user => {
                let userId = user.id || user.uid;
                let userName = user.name || `${user.first_name} ${user.last_name}`;

                dropdown.innerHTML += `<option value="${userId}">${userName}</option>`;
            });
        })
        .catch(error => console.error(`Error loading ${elementId}:`, error));
}

