document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const themeToggle = document.getElementById('theme-toggle');
    
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            document.getElementById('upload-form').submit();
        }
    });

    // Dark/Light theme toggle
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
    });
    
    // Modal close event
    const modal = document.getElementById('qr-modal');
    const modalClose = document.getElementById('modal-close');
    modalClose.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    
    window.addEventListener('click', (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });
});

// Function to show QR code in modal
function showQRCode(filename) {
    const qrImage = document.getElementById('qrImage');
    qrImage.src = '/qrcode/' + encodeURIComponent(filename);
    const modal = document.getElementById('qr-modal');
    modal.style.display = 'block';
}
