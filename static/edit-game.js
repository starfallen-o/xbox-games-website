document.addEventListener("DOMContentLoaded", () => {

    const gameId = window.location.pathname.split('/').pop();
    const toggleEditForm = document.getElementById("toggleEditForm");

    toggleEditForm.addEventListener("click", function () {
        const form = document.getElementById("editGameForm");
        const button = this;

        if (form.style.display === "none") {
            form.style.display = "block";
            button.textContent = "Cancel Edit";
            window.scrollTo({
                top: form.offsetTop,
                behavior: "smooth"
            });
        } else {
            form.style.display = "none";
            button.textContent = "Edit Game";
        }
    });

    document.getElementById('editGameForm').addEventListener("submit", async function (event) {
        event.preventDefault();

        const updatedTitle = document.getElementById("editTitle").value;
        const updatedDescription = document.getElementById("editDescription").value;
        const updatedCost = document.getElementById("editCost").value;
        const updatedReleaseDate = document.getElementById("editReleaseDate").value;
        const updatedGenre = document.getElementById("editGenre").value;
        const updatedPublisher = document.getElementById("editPublisher").value;
        const updatedAgeRating = document.getElementById("editAgeRating").value;

        try {
            const response = await fetch(`/api/v1/games/${gameId}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    title: updatedTitle,
                    description: updatedDescription,
                    cost: updatedCost,
                    release_date: updatedReleaseDate,
                    genre: updatedGenre,
                    publisher: updatedPublisher,
                    age_rating: updatedAgeRating,
                }),
            });

            if (response.ok) {
                alert("Game updated successfully!")
                fetchGameDetails();
                toggleEditForm.click();
            } else {
                const error = await response.json();
                alert(`Error: ${error.message}`);
            }
        } catch (error) {
            console.error("Error updating game: ", error);
            alert("Failed to update game")
        }
    });
});