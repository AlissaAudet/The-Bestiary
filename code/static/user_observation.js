document.addEventListener("DOMContentLoaded", function () {
    const userId = getUserIdFromUrl();
    setupSpeciesSearch();

    document.getElementById("obs-form").addEventListener("submit", async function (event) {
        event.preventDefault();

        const latitude = parseFloat(document.getElementById("latitude").value);
        const longitude = parseFloat(document.getElementById("longitude").value);
        const placeName = document.getElementById("place_name").value.trim() || "Unnamed Place";
        const species = document.getElementById("species").value;

        const pid = await getOrCreatePlace(latitude, longitude, placeName);
        if (!pid) {
            alert("Error: Could not create or find a place.");
            return;
        }

        const observationData = {
            user_id: userId,
            species: species,
            timestamp: document.getElementById("timestamp").value,
            behavior: document.getElementById("behavior").value,
            description: document.getElementById("description").value,
            pid: pid
        };

        try {
            const response = await fetch(`/user/${userId}/observation`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(observationData)
            });

            const result = await response.json();
            alert(result.message || result.error);
            if (response.ok) {
                window.location.href = `/user/${userId}`;
            }
        } catch (error) {
            console.error("Error submitting observation:", error);
            alert("Error submitting observation.");
        }
    });
});

function getUserIdFromUrl() {
    const pathParts = window.location.pathname.split("/");
    return pathParts.includes("user") ? pathParts[pathParts.indexOf("user") + 1] : null;
}

async function getOrCreatePlace(latitude, longitude, placeName) {
    try {
        let response = await fetch(`/api/places/search?latitude=${latitude}&longitude=${longitude}&place_name=${encodeURIComponent(placeName)}`);
        let data = await response.json();

        if (data.exists && data.pid) {
            return data.pid;
        }

        let newPlaceResponse = await fetch("/api/places", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ place_name: placeName, latitude, longitude })
        });

        let newPlaceData = await newPlaceResponse.json();
        return newPlaceData.pid || null;

    } catch (error) {
        console.error("Error finding or creating place:", error);
        return null;
    }
}

function setupSpeciesSearch() {
    const searchInput = document.getElementById("species-search");
    const resultsDropdown = document.getElementById("species-results");
    const hiddenSpeciesInput = document.getElementById("species");

    searchInput.addEventListener("input", async () => {
        const query = searchInput.value.trim();
        if (query.length === 0) {
            resultsDropdown.style.display = "none";
            return;
        }

        try {
            const response = await fetch(`/api/species/search?q=${encodeURIComponent(query)}`);
            const speciesList = await response.json();

            resultsDropdown.innerHTML = "";
            if (speciesList.length === 0) {
                resultsDropdown.style.display = "none";
                return;
            }

            speciesList.forEach(spec => {
                const item = document.createElement("li");
                item.textContent = `${spec.name} (${spec.id})`;
                item.classList.add("dropdown-item");
                item.addEventListener("click", () => {
                    searchInput.value = spec.name;
                    hiddenSpeciesInput.value = spec.id;
                    resultsDropdown.style.display = "none";
                });
                resultsDropdown.appendChild(item);
            });

            resultsDropdown.style.display = "block";
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
