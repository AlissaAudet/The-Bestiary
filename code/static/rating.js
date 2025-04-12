function toggleRating() {
    const section = document.getElementById('rating-section');
    section.style.display = (section.style.display === 'none' || section.style.display === '') ? 'block' : 'none';
}

function updateSliderValue() {
    const slider = document.getElementById('rating-slider');
    document.getElementById('slider-value').innerText = slider.value;
}

function submitRating() {
    const slider = document.getElementById('rating-slider');
    const rating = parseInt(slider.value);

    const observationId = parseInt(document.getElementById('observation-id').value);
    const userId = parseInt(document.getElementById('user-id').value);
    const noteId = Math.floor(Math.random() * 100000);  // Simulating an ID; replace with actual logic if needed

    const payload = {
        nid: noteId,
        obersation_oid: observationId,
        "user.uid": userId,
        note: rating
    };

    fetch(`/observation/${observationId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
        } else {
            alert("Error: " + (data.error || "Unknown error"));
        }
    })
    .catch(err => {
        console.error(err);
        alert("Something went wrong submitting the rating.");
    });
}
