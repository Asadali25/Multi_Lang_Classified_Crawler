document.addEventListener('DOMContentLoaded', function () {

let ExcBtn = document.getElementById('exc-btn');
let formDiv = document.querySelector('.myform');
let MainTitle = document.getElementById('main-title');
let successGif = document.getElementById('success-gif');
let processingGif = document.getElementById('processing-gif');
let perDiv = document.querySelector('.percentage-input');
let qaInput = document.getElementById('qainput');
let fullfile = document.getElementById('completefile');
let download = document.getElementById('download-btn');





ExcBtn.addEventListener('click', function () {
    successGif.style.display = 'none';
    MainTitle.textContent = 'Please Fill the Form';
    formDiv.classList.remove('hidden');
    if (ExcBtn.textContent === 'Start Excecution') {
        formDiv.classList.add('hidden');
        ExcBtn.classList.add('hidden');
        processingGif.style.display = 'block';
        MainTitle.textContent = ' FIle is Processing...';
        sendForm();
    }
    ExcBtn.textContent = 'Start Excecution';

});

// Form Handeling
 function sendForm() {
    console.log('Form submitted');
    let formobj = {
        'qaInput': qaInput.checked,
        'fullfile': fullfile.checked,
        'percentage': perDiv.querySelector('input').value,
        'prompt': document.getElementById('prompt').value
    };
    // send data to backend 
    fetch('/form', {
        method: 'POST',
        body: JSON.stringify(formobj),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(function (response) {
        if (response.ok) {
            // Hide form and show success GIF
            formDiv.classList.add('hidden');
            MainTitle.textContent = 'File is ready to download';
            processingGif.style.display = 'none';
            successGif.style.display = 'block';
            download.classList.remove('hidden');
            
        } else {
            throw new Error('Form submission failed');
        }
    })
    .catch(function (error) {
        console.error(error);
        MainTitle.textContent = 'Error in processing file';
    });
}

// Inputs radios
qaInput.addEventListener('change', function () {
    if (qaInput.checked) {
        perDiv.classList.remove('hidden');
    }
});
fullfile.addEventListener('change', function () {
    if (fullfile.checked) {
        perDiv.classList.add('hidden');
    }
});


});