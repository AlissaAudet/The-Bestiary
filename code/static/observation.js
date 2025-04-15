document.getElementById("obs-form").addEventListener("input", fetchFilteredObservations);
document.getElementById("obs-form").addEventListener("click", fetchFilteredObservations);

setupSpeciesSearch()
fetchFilteredObservations();

async function fetchFilteredObservations() {
    const author = document.getElementById("author-search").value;
    const species = document.getElementById("species").value;
    const behaviorInput = document.getElementById("behavior").value;
    const behavior = (behaviorInput === "None") ? "" : behaviorInput;
    const timestamp = document.getElementById("timestamp").value;
    const place_name = document.getElementById("place_name").value;

    const resultsContainer = document.getElementById("search-results");
    const queryParams = new URLSearchParams({
        author: author || "",
        species: species || "",
        behavior: behavior || "",
        timestamp: timestamp || "",
        place_name: place_name || "",
    });

    try {
        const response = await fetch(`/api/observations/filter?${queryParams}`);
        const observations = await response.json();

        resultsContainer.innerHTML = "";

        const maxToShow = 10;
        const visible = observations.slice(0, maxToShow);
        const hidden = observations.slice(maxToShow);

        visible.forEach(obs => {
            const li = document.createElement("li");
            li.textContent = `${obs.species} - ${obs.author} - ${obs.behavior}`;
            li.classList.add("dropdown-item");
            li.addEventListener("click", function () {
                window.location.href = `/observation/${obs.oid}`;
            });
            resultsContainer.appendChild(li);
        });

        if (hidden.length > 0) {
            const loadMoreBtn = document.createElement("button");
            loadMoreBtn.textContent = "Load more";
            loadMoreBtn.style.border = "none";

            loadMoreBtn.addEventListener("click", () => {
                hidden.forEach(obs => {
                    const li = document.createElement("li");
                    li.textContent = `${obs.species} - ${obs.author} - ${obs.behavior}`;
                    li.classList.add("dropdown-item");
                    li.addEventListener("click", function () {
                        window.location.href = `/observation/${obs.oid}`;
                    });
                    resultsContainer.appendChild(li);
                });
                loadMoreBtn.remove();
            });

            resultsContainer.appendChild(loadMoreBtn);
        }

        resultsContainer.style.setProperty("display", observations.length ? "block" : "none", "important");

    } catch (error) {
        console.error("Error fetching filtered observations:", error);
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

    document.getElementById("species-search").addEventListener("click", function() {
        hiddenSpeciesInput.value = ""
        searchInput.value = "";
})
}