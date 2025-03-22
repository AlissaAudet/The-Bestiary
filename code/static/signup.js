document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("auth-form");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const userData = {
            first_name: document.getElementById("first-name").value,
            last_name: document.getElementById("last-name").value,
            email: document.getElementById("email").value,
            age: document.getElementById("age").value,
            user_type: document.getElementById("user-type").value
        };

        fetch("signup", {
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
            }
        })
        .catch(error => console.error("Error:", error));
    });
});
