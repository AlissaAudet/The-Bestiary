document.addEventListener("DOMContentLoaded", function () {
    const userId = getUserIdFromUrl();
    setupSpeciesSearch();

    document.getElementById("obs-form").addEventListener("submit", async function (event) {
        event.preventDefault();

        const latitude = parseFloat(document.getElementById("latitude").value);
        const longitude = parseFloat(document.getElementById("longitude").value);
        const placeName = document.getElementById("place_name").value.trim() || "Unnamed Place";
        const species = document.getElementById("species").value;
        const imageInput = document.getElementById("image");

        const pid = await getOrCreatePlace(latitude, longitude, placeName);
        if (!pid) {
            alert("Error: Could not create or find a place.");
            return;
        }

        const photo_id = await createImage(imageInput)

        console.log(photo_id)

        const formData = new FormData();
        formData.append("user_id", userId);
        formData.append("species", species);
        formData.append("timestamp", document.getElementById("timestamp").value);
        formData.append("behavior", document.getElementById("behavior").value);
        formData.append("description", document.getElementById("description").value);
        formData.append("pid", pid);
        formData.append("photo_id", photo_id)

        try {
            const response = await fetch(`/user/${userId}/observation`, {
                method: "POST",
                body: formData
            });

            const result = await response.json();
            console.log("Server response:", result);
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
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({place_name: placeName, latitude, longitude})
        });

        let newPlaceData = await newPlaceResponse.json();
        return newPlaceData.pid || null;

    } catch (error) {
        console.error("Error finding or creating place:", error);
        return null;
    }
}

async function createImage(imageInput) {
    const file = imageInput.files[0];
    if (!file) {
        alert("Please select an image before submitting.");
        return null;
    }

    const formData = new FormData();
    formData.append("image", file);

    try {
        const response = await fetch("/api/photo", {
            method: "POST",
            body: formData
        });

        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            const text = await response.text();
            console.error("Invalid JSON response:", text);
            throw new Error("Invalid JSON response from /api/photo");
        }

        const data = await response.json();
        return data.photo_id || null;

    } catch (error) {
    console.error("Error creating photo:", error);
    alert("Failed to upload image. Please try again.");
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
