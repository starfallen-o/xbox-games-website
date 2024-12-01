document.addEventListener("DOMContentLoaded", () => {

    const gameId = window.location.pathname.split('/').pop();

    const toggleUploadMediaForm = document.getElementById('toggleUploadMediaForm');

    // Toggle Upload Form
    toggleUploadMediaForm.addEventListener("click", function () {
        const form = document.getElementById('uploadMediaForm');
        const button = this;

        if (form.style.display === "none") {
            form.style.display = "block";
            button.textContent = "Cancel Upload";
            window.scrollTo({
                top: form.offsetTop,
                behavior: "smooth"
            });
        } else {
            form.style.display = "none";
            button.textContent = "Upload Media";
        }
    });

    // Add Media
    document.getElementById('uploadMediaForm').addEventListener("submit", async function (event) {
        event.preventDefault();

        const mediaFileInput = document.getElementById("mediaFile");
        if (mediaFileInput.files.length === 0) {
            alert("Please select a media file to upload.");
            return;
        }

        const formData = new FormData();
        formData.append("mediaFile", mediaFileInput.files[0]);
        formData.append("gameId", gameId);

        try {
            const response = await fetch(`/api/v1/games/${gameId}`, {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                alert("Media file uploaded successfully!");
                mediaFileInput.value = "";
                fetchGameDetails();
                toggleUploadMediaForm.click();
            } else {
                const error = await response.json();
                alert(`Error: ${error.message}`);
            }
        } catch (error) {
            console.error("Error uploading media:", error);
            alert("Failed to upload media file.");
        }
    });
});