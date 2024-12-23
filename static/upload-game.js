document.addEventListener("DOMContentLoaded", () => {

    // Toggle Upload Form
    const form = document.getElementById("uploadForm");
    const toggleUploadForm = document.getElementById("toggleUploadForm");

    toggleUploadForm.addEventListener("click", function () {
        const button = this;

        if (form.style.display === "none") {
            form.style.display = "block";
            button.textContent = "Cancel";
            window.scrollTo({
                top: form.offsetTop,
                behavior: "smooth"
            });
        } else {
            form.style.display = "none";
            button.textContent = "Upload A Game";
        }
    });


    // Upload a new game
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const files = document.getElementById("files").files;

        for (let i = 0; i < files.length; i++) {
            formData.append("files[]", files[i]);
        }

        const response = await fetch('api/v1/games', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            alert("Game uploaded successfully!");
            form.reset();
            loadGames();
            toggleUploadForm.click();
        } else {
            alert("Failed to upload game.")
        }
    });

    loadGames();
});