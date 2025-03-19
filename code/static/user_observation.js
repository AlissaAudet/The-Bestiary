document.addEventListener("DOMContentLoaded", () => {
    setupPlaceForm();
    setupSpeciesSearch();
});

function setupPlaceForm() {
    const submitButton = document.querySelector("button[type='submit']");
    if (submitButton) {
        submitButton.addEventListener("click", async (event) => {
            event.preventDefault();
            await handlePlaceSubmission();
        });
    }
}

async function handlePlaceSubmission() {
    const latitude = document.getElementById("latitude").value.trim();
    const longitude = document.getElementById("longitude").value.trim();
    const placeName = document.getElementById("place_name").value.trim();

    if (!validateCoordinates(latitude, longitude)) {
        alert("Please enter valid coordinates.");
        return;
    }

    try {
        const exists = await checkIfPlaceExists(latitude, longitude, placeName);
        if (exists) {
            alert("This place already exists in the database!");
        } else {
            await addNewPlace(latitude, longitude, placeName);
            alert("Place added successfully!");
            window.location.reload();
        }
    } catch (error) {
        console.error("Error adding place:", error);
        alert("An error occurred. Please try again.");
    }
}

function validateCoordinates(lat, lng) {
    return (
        lat !== "" &&
        lng !== "" &&
        !isNaN(lat) &&
        !isNaN(lng) &&
        lat >= -90 &&
        lat <= 90 &&
        lng >= -180 &&
        lng <= 180
    );
}

async function checkIfPlaceExists(latitude, longitude, placeName) {
    try {
        const response = await fetch(`/api/places/search?latitude=${latitude}&longitude=${longitude}&place_name=${encodeURIComponent(placeName)}`);
        if (!response.ok) {
            throw new Error("Failed to check if place exists");
        }
        const data = await response.json();
        return data.exists;
    } catch (error) {
        console.error("Error checking place existence:", error);
        return false;
    }
}

async function addNewPlace(latitude, longitude, placeName) {
    try {
        const response = await fetch("/api/places", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ place_name: placeName, latitude, longitude })
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.message || "Unknown error");
        }
    } catch (error) {
        console.error("Error adding place:", error);
        throw error;
    }
}

function setupSpeciesSearch() {
    const searchInput = document.getElementById("species-search");
    const resultsDropdown = document.getElementById("species-results");

    if (!searchInput || !resultsDropdown) {
        console.error("Species search elements not found!");
        return;
    }

    console.log("Species search initialized!"); // Debug log

    searchInput.addEventListener("input", async () => {
        const query = searchInput.value.trim();
        console.log(`User typed: ${query}`); // Debug log

        if (query.length === 0) {
            resultsDropdown.style.display = "none";
            return;
        }

        try {
            const species = await searchSpecies(query);
            displaySpeciesResults(species, resultsDropdown, searchInput);
        } catch (error) {
            console.error("Error fetching species:", error);
        }
    });

    document.addEventListener("click", (event) => {
        if (!resultsDropdown.contains(event.target) && event.target !== searchInput) {
            resultsDropdown.style.display = "none";
        }
    });
}

async function searchSpecies(query) {
    try {
        console.log(`Fetching species for query: ${query}`); // Debugging log
        const response = await fetch(`/api/species/search?q=${encodeURIComponent(query)}`);

        if (!response.ok) {
            throw new Error(`Failed to fetch species: ${response.statusText}`);
        }

        const data = await response.json();
        console.log("API response:", data); // Debugging log
        return data;
    } catch (error) {
        console.error("Error fetching species:", error);
        return [];
    }
}

function displaySpeciesResults(species, dropdown, searchInput) {
    dropdown.innerHTML = ""; // Clear previous results

    if (species.length === 0) {
        dropdown.style.display = "none";
        return;
    }

    species.forEach((spec) => {
        const item = document.createElement("li");
        item.textContent = `${spec.name} (${spec.id})`;
        item.classList.add("dropdown-item");

        // Clicking on an item fills the input field
        item.addEventListener("click", () => {
            searchInput.value = spec.name; // Set input value to species name
            dropdown.style.display = "none"; // Hide dropdown
        });

        dropdown.appendChild(item);
    });

    dropdown.style.display = "block";
}