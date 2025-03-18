document.addEventListener("DOMContentLoaded", function () {
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
        goToUserButton.disabled = true;
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

        users.forEach(user => {
            const li = document.createElement("li");
            li.textContent = user.name;
            li.dataset.userId = user.id;
            li.classList.add("user-item");

            li.addEventListener("click", function () {
                searchInput.value = this.textContent;
                selectedUserId = this.dataset.userId;
                goToUserButton.disabled = false;
                resultsContainer.style.display = "none";
            });

            resultsContainer.appendChild(li);
        });
    } catch (error) {
        console.error("Error fetching users:", error);
    }
});


    goToUserButton.addEventListener("click", function () {
        console.log("Redirecting to user:", selectedUserId); // 🛠 Debug

        if (selectedUserId) {
            window.location.href = `/user/${selectedUserId}`;
        } else {
            console.error(" user selected for redirection.");
        }
    });

    document.addEventListener("click", function (event) {
        if (!resultsContainer.contains(event.target) && event.target !== searchInput) {
            resultsContainer.style.display = "none";
        }
    });
});
