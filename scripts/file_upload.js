/**
 * Manejo de carga de archivos para formulario de carreras
 */

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('cv_file');
    const fileUploadDisplay = document.querySelector('.file_upload_display');
    const fileUploadText = document.querySelector('.file_upload_text');
    const fileName = document.getElementById('file_name');

    if (fileInput && fileUploadDisplay) {
        // Hacer clic en el área de carga active el input de archivo
        fileUploadDisplay.addEventListener('click', function() {
            fileInput.click();
        });

        // Manejar cambio de archivo
        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            
            if (file) {
                // Validar tipo de archivo
                const allowedTypes = [
                    'application/pdf',
                    'application/msword',
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                ];
                
                if (!allowedTypes.includes(file.type)) {
                    showMessage('Por favor selecciona un archivo PDF, DOC o DOCX', 'error');
                    this.value = '';
                    resetFileDisplay();
                    return;
                }

                // Validar tamaño de archivo (máximo 5MB)
                const maxSize = 5 * 1024 * 1024; // 5MB en bytes
                if (file.size > maxSize) {
                    showMessage('El archivo es demasiado grande. Máximo 5MB permitido.', 'error');
                    this.value = '';
                    resetFileDisplay();
                    return;
                }

                // Mostrar archivo seleccionado
                fileUploadDisplay.classList.add('has_file');
                fileUploadText.textContent = '✓ Archivo seleccionado';
                fileName.textContent = file.name;
            } else {
                resetFileDisplay();
            }
        });

        // Manejar drag & drop
        fileUploadDisplay.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.style.borderColor = 'var(--color_orange)';
            this.style.backgroundColor = 'rgba(255, 255, 255, 1)';
        });

        fileUploadDisplay.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.style.borderColor = '#e2e8f0';
            this.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
        });

        fileUploadDisplay.addEventListener('drop', function(e) {
            e.preventDefault();
            this.style.borderColor = '#e2e8f0';
            this.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                fileInput.dispatchEvent(new Event('change'));
            }
        });
    }

    function resetFileDisplay() {
        if (fileUploadDisplay && fileUploadText && fileName) {
            fileUploadDisplay.classList.remove('has_file');
            fileUploadText.textContent = '📄 Seleccionar archivo';
            fileName.textContent = '';
        }
    }

    function showMessage(message, type) {
        const messageElement = document.getElementById('careers_form_msg');
        if (messageElement) {
            messageElement.textContent = message;
            messageElement.className = `form_msg ${type} active`;
            
            setTimeout(() => {
                messageElement.classList.remove('active');
            }, 5000);
        }
    }
});