document.getElementById("post_comment_btn").addEventListener("click", async function () {
    const commentBox = document.getElementById("comment_box");
    const commentText = commentBox.value.trim();
    const observationId = window.location.pathname.split("/")[2];


    if (commentText.length > 0) {
        try {
            const response = await fetch(`/api/observation/${observationId}/comment`, {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams({
                    comment_text: commentText
                })
            });

            const data = await response.json();
            if (data.message === "Comment posted successfully") {
                commentBox.value = "";
                await fetchComments();
            } else {
                alert(data.error || "Error posting comment");
            }
        } catch (error) {
            console.error("Error posting comment:", error);
        }
    } else {
        alert("Please enter a comment before submitting.");
    }
});

async function fetchComments() {
    const observationId = window.location.pathname.split("/")[2];

    try {
        const response = await fetch(`/api/observation/${observationId}/comments`);
        const comments = await response.json();

        console.log("Fetched comments:", comments);

        const commentList = document.getElementById("comment-list");
        commentList.innerHTML = "";

        if (comments && Array.isArray(comments)) {
            comments.forEach(comment => {
                const li = document.createElement("li");
                li.textContent = `${comment.first_name} ${comment.last_name}: ${comment.text}`;
                commentList.appendChild(li);
            });
        } else {
            console.error("Expected an array but got:", comments);
        }
    } catch (error) {
        console.error("Error fetching comments:", error);
    }
}


document.addEventListener("DOMContentLoaded", fetchComments);