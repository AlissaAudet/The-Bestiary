document.addEventListener("DOMContentLoaded", function () {
    let currentIndex = 0;
    let observations = [];

    async function loadCarousel() {
        try {
            const response = await fetch("/api/observations/latest");
            const data = await response.json();
            observations = data;

            const image = document.getElementById("carousel-image");
            if (!image) return;

            showSlide(currentIndex);
        } catch (e) {
            console.error("Error loading carousel data:", e);
        }
    }

    function showSlide(index) {
        const image = document.getElementById("carousel-image");
        if (observations.length === 0 || !image) return;

        const obs = observations[index];
        image.src = `data:image/jpeg;base64,${obs.image_data}`;
        image.onclick = () => window.location.href = `/observation/${obs.oid}`;
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + observations.length) % observations.length;
        showSlide(currentIndex);
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % observations.length;
        showSlide(currentIndex);
    }

    window.prevSlide = prevSlide;
    window.nextSlide = nextSlide;

    loadCarousel();

    const searchInput = document.getElementById("user-search");
    const resultsContainer = document.getElementById("user-results");
    const goToUserButton = document.getElementById("go-to-user");

    let selectedUserId = null;

searchInput.addEventListener("input", async function () {
    const query = searchInput.value.replace(/\s+/g, " ").trim();

    if (query.length < 1) {
        resultsContainer.innerHTML = "";
        resultsContainer.style.display = "none";
        selectedUserId = null;
        if (goToUserButton) goToUserButton.disabled = true;
        return;
    }

    try {
        const response = await fetch(`/api/users/search?q=${encodeURIComponent(query)}`);
        const users = await response.json();
        console.log("Users fetched:", users);

        resultsContainer.innerHTML = "";

        if (users.length === 0) {
            resultsContainer.style.display = "none";
            return;
        }

        resultsContainer.style.display = "block";

        users.slice(0, 5).forEach(user => {
            const li = document.createElement("li");
            li.textContent = user.name;
            li.dataset.userId = user.id;
            li.classList.add("dropdown-item");

            li.addEventListener("click", function () {
                selectedUserId = this.dataset.userId;
                window.location.href = `/user/${selectedUserId}`;
            });

            resultsContainer.appendChild(li);
        });
    } catch (error) {
        console.error("Error fetching users:", error);
    }
});

});
