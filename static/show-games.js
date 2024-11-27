document.addEventListener("DOMContentLoaded", () => {

    // Show all games
    async function loadGames() {
        const response = await fetch('/api/v1/games');
        const games = await response.json();
        const gamesList = document.getElementById("gameList")

        gamesList.innerHTML = '';
        games.forEach(game => {
            const gameCard = document.createElement('div');
            gameCard.classList.add('col');

            mediaHtml= `<img src="${game.media[0]}" class="img-fluid mb-2" alt="${game.title}" style="max-height: 150px;"`

            gameCard.innerHTML = `
                <div class="card h-100">
                    <a href="/games/${game.id}" class="text-decoration-none text-dark">
                        <div class="card-img-top text-center">${mediaHtml}</div>
                        <div class="card-body">
                            <h5 class="card-title text-center">${game.title}</h5>
                            <p class="card-text text-center">${game.genre}</p>
                            <p class="card-text text-center">£${game.cost}</p>
                        </div>
                    </a>
                </div>
            `;

            gameList.appendChild(gameCard);

        });
    }

    loadGames();
});