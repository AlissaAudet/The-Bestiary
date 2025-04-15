document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signup-form");
    if (signupForm) {
        signupForm.addEventListener("submit", signup);
    }

    const followerContainer = document.getElementById("follower-container");
    const followBtn = document.getElementById("follow-btn");

    if (followerContainer || followBtn) {
        const profileUid = getUserIdFromUrl();

        fetchFollowers(profileUid);
        fetchFollowing(profileUid);

        fetch("/check_auth", { credentials: "include" })
            .then(res => res.json())
            .then(auth => {
                if (followBtn) {
                    if (!auth.authenticated || auth.user_id === profileUid) {
                        followBtn.style.display = "none";
                    } else {
                        fetch(`/is_following/${profileUid}`, { credentials: "include" })
                            .then(res => res.json())
                            .then(data => {
                                followBtn.textContent = data.is_following ? "Unfollow" : "Follow";
                                followBtn.dataset.following = data.is_following.toString();
                            });
                    }
                }
            });
    }
});

async function signup(event) {
    event.preventDefault();

    const firstName = document.getElementById("first-name").value.trim();
    const lastName = document.getElementById("last-name").value.trim();
    const email = document.getElementById("email").value.trim();
    const age = parseInt(document.getElementById("age").value);
    const userType = document.getElementById("user-type").value;
    const password = document.getElementById("password").value.trim();

    const nameRegex = /^[A-Za-zÀ-ÿ\s\-']+$/;
    if (!nameRegex.test(firstName) || !nameRegex.test(lastName)) {
        alert("First name and last name must not contain numbers or symbols.");
        return;
    }

    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    const digits = password.match(/\d/g);
    const hasTwoDigits = digits && digits.length >= 2;

    if (password.length < 7 || !hasSpecialChar || !hasTwoDigits) {
        alert("Password must be at least 7 characters long, include 1 special character and 2 digits.");
        return;
    }

    const userData = {
        first_name: firstName,
        last_name: lastName,
        email: email,
        age: age,
        user_type: userType,
        password: password
    };

    fetch("/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData)
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
            } else {
                alert("User successfully registered!");
                document.getElementById("signup-form").reset();
                window.location.href = "/login";
            }
        })
        .catch(error => {
            console.error("Request failed:", error);
            alert("An error occurred. Please try again.");
        });
}

async function login(event) {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const result = await response.json();

        if (response.ok) {
            alert("Login successful!");
            window.location.href = `/user/${result.user_id}`;
        } else {
            alert("Error: " + (result.message || "Invalid email or password."));
        }
    } catch (error) {
        console.error("Login error:", error);
        alert("An error occurred. Please try again.");
    }
}

async function logout() {
    try {
        const response = await fetch("/logout", {
            method: "POST",
            credentials: "include"
        });

        const result = await response.json();

        if (response.ok) {
            alert("Logged out successfully!");
            window.location.href = "/login";
        } else {
            alert("Logout failed: " + result.message);
        }
    } catch (error) {
        console.error("Logout error:", error);
        alert("An error occurred. Please try again.");
    }
}

async function checkAuth() {
    try {
        const response = await fetch("/check_auth", { method: "GET", credentials: "include" });
        const result = await response.json();
        return result.authenticated;
    } catch (error) {
        console.error("Auth check error:", error);
        return false;
    }
}

async function toggleFollow(targetUid) {
    try {
        const button = document.getElementById("follow-btn");
        const isFollowing = button.dataset.following === "true";

        const url = isFollowing ? `/unfollow/${targetUid}` : `/follow/${targetUid}`;
        const response = await fetch(url, {
            method: "POST",
            credentials: "include"
        });

        const result = await response.json();

        if (response.ok) {
            button.textContent = isFollowing ? "Follow" : "Unfollow";
            button.dataset.following = (!isFollowing).toString();

            const profileUid = getUserIdFromUrl();
            await fetchFollowers(profileUid);
            await fetchFollowing(profileUid);
        } else {
            alert(result.error || "Failed to update follow status.");
        }
    } catch (error) {
        console.error("Follow/unfollow error:", error);
        alert("An error occurred while updating follow status.");
    }
}

function getUserIdFromUrl() {
    const parts = window.location.pathname.split("/");
    return parseInt(parts[2]);
}

async function fetchFollowers(uid) {
    try {
        const response = await fetch(`/api/followers/${uid}`);
        const followers = await response.json(); // <- c'est ici qu'on a déjà les données
        renderUserList(followers, "followers-list", "See more followers...", "No followers yet");
    } catch (e) {
        console.error("Erreur chargement followers:", e);
    }
}

async function fetchFollowing(uid) {
    try {
        const response = await fetch(`/api/following/${uid}`);
        const following = await response.json(); // <- pareil ici
        renderUserList(following, "following-list", "See more following...", "Not following anyone yet");
    } catch (e) {
        console.error("Erreur chargement following:", e);
    }
}


function renderUserList(users, containerId, moreText, emptyMessage) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = "";

    if (!Array.isArray(users) || users.length === 0) {
        const li = document.createElement("li");
        li.textContent = emptyMessage || "No data found";
        li.style.fontStyle = "italic";
        li.style.color = "#777";
        container.appendChild(li);
        return;
    }

    const maxToShow = 5;
    const visible = users.slice(0, maxToShow);
    const hidden = users.slice(maxToShow);

    for (const user of visible) {
        const li = document.createElement("li");
        li.textContent = `${user.first_name} ${user.last_name}`;
        container.appendChild(li);
    }

    if (hidden.length > 0) {
        const moreBtn = document.createElement("button");
        moreBtn.textContent = moreText;
        moreBtn.onclick = () => {
            for (const user of hidden) {
                const li = document.createElement("li");
                li.textContent = `${user.first_name} ${user.last_name}`;
                container.appendChild(li);
            }
            moreBtn.remove();
        };
        container.appendChild(moreBtn);
    }
}

