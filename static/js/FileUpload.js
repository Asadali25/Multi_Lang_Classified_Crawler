document.addEventListener('DOMContentLoaded', function () {
    let fileInput = document.getElementById('file-input');
    let loadingGif = document.getElementById('loading-gif');
    let successGif = document.getElementById('success-gif');
    let MainTitle = document.getElementById('main-title');
    let InputContainer = document.getElementById('upload-container');
    let ExcBtnDiv = document.querySelector('.exc-button');
    

    fileInput.addEventListener('change', function () {
        var file = fileInput.files[0];
        var formData = new FormData();
        formData.append('file', file);

        // Display loading GIF
        InputContainer.style.display= 'none'
        MainTitle.textContent = 'File is Uploading...'
        loadingGif.style.display = 'block';

        // Upload file
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(function (response) {
            if (response.ok) {
                // Hide loading GIF and show success GIF
                loadingGif.style.display = 'none';
                MainTitle.textContent = 'File Uploaded Successfully'
                successGif.style.display = 'block';
                ExcBtnDiv.classList.remove('hidden');
            } else {
                throw new Error('Upload failed');
            }
        })
        .catch(function (error) {
            console.error(error);
            // Handle upload error
        });
    });
});
