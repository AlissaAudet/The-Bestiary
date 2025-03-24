document.addEventListener("DOMContentLoaded", async function () {
    const userId = window.location.pathname.split("/")[2];
    const observationsContainer = document.getElementById("observations-container");

    try {
        const response = await fetch(`/api/user/${userId}/observations`);
        const observations = await response.json();

        if (observations.length === 0) {
            observationsContainer.innerHTML = "<p>No past observations found.</p>";
            return;
        }

        const observationList = document.createElement("ul");

        observations.forEach(obs => {
            const listItem = document.createElement("li");
            const link = document.createElement("a");

            link.href = `/observation/${obs.oid}`;
            link.textContent = `Observation #${obs.oid} - ${obs.species} - ${obs.timestamp}`;

            listItem.appendChild(link);
            observationList.appendChild(listItem);
        });

        observationsContainer.innerHTML = "";
        observationsContainer.appendChild(observationList);
    } catch (error) {
        console.error("Error fetching observations:", error);
        observationsContainer.innerHTML = "<p>Error loading observations.</p>";
    }
});
