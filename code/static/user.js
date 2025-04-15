document.addEventListener("DOMContentLoaded", async function () {
    const userId = window.location.pathname.split("/")[2];
    const observationsContainer = document.getElementById("observations-container");

    let observations = [];
    let shownCount = 0;
    const batchSize = 10;

    try {
        const response = await fetch(`/api/user/${userId}/observations`);
        observations = await response.json();

        if (observations.length === 0) {
            observationsContainer.innerHTML = "<p>No past observations found.</p>";
            return;
        }

        const observationList = document.createElement("ul");
        observationList.id = "observation-list";
        observationsContainer.appendChild(observationList);

        const loadMoreBtn = document.createElement("button");
        loadMoreBtn.textContent = "Load more";
        loadMoreBtn.classList.add("return-btn");
        loadMoreBtn.style.border = "none";
        loadMoreBtn.addEventListener("click", showMoreObservations);

        function showMoreObservations() {
            const nextBatch = observations.slice(shownCount, shownCount + batchSize);

            nextBatch.forEach(obs => {
                const listItem = document.createElement("li");
                const link = document.createElement("a");

                link.href = `/observation/${obs.oid}`;
                link.textContent = `Observation #${obs.oid} - ${obs.species} - ${obs.timestamp}`;

                listItem.appendChild(link);
                observationList.appendChild(listItem);
            });

            shownCount += nextBatch.length;

            if (shownCount >= observations.length) {
                loadMoreBtn.remove();
            }
        }

        showMoreObservations();
        if (observations.length > batchSize) {
            observationsContainer.appendChild(loadMoreBtn);
        }

    } catch (error) {
        console.error("Error fetching observations:", error);
        observationsContainer.innerHTML = "<p>Error loading observations.</p>";
    }
});
