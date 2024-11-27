document.addEventListener("DOMContentLoaded", () => {

    const gameId = window.location.pathname.split('/').pop();
    
    async function fetchGameDetails(){
        const response = await fetch(`/api/v1/games/${gameId}`);
        if (response.ok) {
            const game = await response.json();


            document.getElementById('editTitle').value = game.title;
            document.getElementById('editDescription').value = game.description;
            document.getElementById('editCost').value = game.cost;
            document.getElementById('editReleaseDate').value = game.release_date;
            document.getElementById('editGenre').value = game.genre;
            document.getElementById('editPublisher').value = game.publisher;
            document.getElementById('editAgeRating').value = game.age_rating;

            displayGameDetails(game);

            document.querySelectorAll(".delete-media-button").forEach(button => {
                button.addEventListener("click", async (event) => {
                    const mediaUrl = event.target.getAttribute("data-url");
                    if(confirm("Are you sure you want to delete this media?")) {
                        await deleteMedia(gameId, mediaUrl);
                    }
                });
            });

            document.getElementById("deleteGameButton").addEventListener("click", async (event) => {
                if(confirm("Are you sure you want to delete this game and its media?")) {
                    await deleteGame(gameId);
                }
            });

        } else {
            document.getElementById('gameTitle').textContent = 'Game Not Found';
        }
    }

    function displayGameDetails(game) {
        document.getElementById('gameTitle').textContent = game.title;

        let mediaHtml = '';
        game.media.forEach(url => {
            mediaHtml += `<img src="${url}" class="img-fluid m-2" alt="${game.title}" style="max-height: 200px;">`;
        });

        const detailsHtml = `
            <p><strong>Description:</strong> ${game.description}</p>
            <p><strong>Cost:</strong> £${game.cost}</p>
            <p><strong>Release Date:</strong> ${game.release_date}</p>
            <p><strong>Genre:</strong> ${game.genre}</p>
            <p><strong>Publisher:</strong> ${game.publisher}</p>
            <p><strong>Age Rating:</strong> ${game.age_rating}</p>
            <br>
            <h5 class="bg-primary text-light p-2">Media<h5>
        `;

        document.getElementById('gameDetails').innerHTML = detailsHtml;

        const mediaSection = document.getElementById('mediaSection');
        mediaSection.innerHTML = "";
        game.media.forEach(url => {
            const mediaName = url.split('_').pop();
            const mediaElement = `
                <div class="col">
                    <div class="card">
                        <img src="${url}" class="card-img-top" alt="${mediaName}">
                        <div class="card-body">
                            <p class="card-text text-center">${mediaName}</p>
                        </div>
                        <button class="btn btn-danger btn-sm delete-media-button text-center" data-url="${url}">Delete</button>
                    </div>
                </div>
            `;

            mediaSection.innerHTML += mediaElement;
        });
    }

    async function deleteMedia(gameId, mediaUrl) {
        const response = await fetch(`/api/v1/games/${gameId}/media`, {
            method: 'DELETE',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({media_url: mediaUrl})
        });

        if (response.ok) {
            alert("Media deleted successfully");
            await fetchGameDetails();
        } else {
            alert("Failed to delete media");
        }
    }

    async function deleteGame(gameId) {
        const response = await fetch(`/api/v1/games/${gameId}`, {
            method: 'DELETE',
            headers: {'Content-Type': 'application/json'}
        });

        if (response.ok) {
            alert("Game and its media have been deleted successfully");
            window.location.href = '/games';
        } else {
            const error = await response.json();
            alert(`Failed to delete game: ${error.message}`);
        }
    }

    fetchGameDetails();

});