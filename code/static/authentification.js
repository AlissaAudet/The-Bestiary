
document.addEventListener("DOMContentLoaded", function() {
    const signupForm = document.getElementById("signup-form");
    if (signupForm) {
        signupForm.addEventListener("submit", signup);
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("signup-form");

    form.addEventListener("submit", function (event) {
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
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
            } else {
                alert("User successfully registered!");
                form.reset();
                window.location.href = "/login";
            }
        })
        .catch(error => {
            console.error("Request failed:", error);
            alert("An error occurred. Please try again.");
        });
    });
});

async function login(event) {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    console.log("Trying to login with:", { email, password });

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const result = await response.json();
        console.log("Server response:", result);

        if (response.ok) {
            alert("Login successful!");
            window.location.href = `/user/${result.user_id}`;
        } else {
            alert("Error: " + (result.message || "Invalid email or password. Please try again."));
        }
    } catch (error) {
        console.error("Request failed", error);
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
        console.log("Logout response:", result);

        if (response.ok) {
            alert("Logged out successfully!");
            window.location.href = "/login";
        } else {
            alert("Logout failed: " + result.message);
        }
    } catch (error) {
        console.error("Logout request failed", error);
        alert("An error occurred. Please try again.");
    }
}

async function checkAuth() {
    console.log("Checking authentication via server...");

    try {
        const response = await fetch("/check_auth", { method: "GET", credentials: "include" });
        const result = await response.json();
        console.log("Auth check response:", result);

        return result.authenticated;
    } catch (error) {
        console.error("Authentication check failed:", error);
        return false;
    }
}

async function checkAuthAndUser() {
    console.log("Checking authentication via server...");

    try {
        const response = await fetch("/check_auth", { method: "GET", credentials: "include" });
        const result = await response.json();
        console.log("Auth check response:", result);

        if (!result.authenticated) {
            return { authenticated: false, authorized: false };
        }

        const urlParts = window.location.pathname.split("/");
        if (urlParts[1] === "user" && !isNaN(parseInt(urlParts[2]))) {
            const profileUid = parseInt(urlParts[2]);
            const userId = result.user_id;

            console.log("URL UID:", profileUid, "| Authenticated UID:", userId);

            return { authenticated: true, authorized: userId === profileUid };
        }

        return { authenticated: true, authorized: false };
    } catch (error) {
        console.error("Authentication check failed:", error);
        return { authenticated: false, authorized: false };
    }
}
