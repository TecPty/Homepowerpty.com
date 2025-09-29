/**
 * Manejo de formularios de contacto y carreras
 * Versión unificada simplificada sin CSRF token
 */

(function(){
    // Formulario de contacto
    const contactForm = document.getElementById('form');
    const contactMsg = document.getElementById('form_msg');
    
    // Formulario de carreras
    const careersForm = document.getElementById('careers_form');
    const careersMsg = document.getElementById('careers_form_msg');

    // Validación en tiempo real
    function validateField(field, value) {
        switch(field) {
            case 'name':
            case 'full_name':
                return value.trim().length >= 2;
            case 'number':
            case 'phone':
                return /^[\d\s\+\-\(\)]{7,}$/.test(value.trim());
            case 'message':
                return value.trim().length >= 10;
            case 'email':
                return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
            case 'position':
                return value.length > 0;
            case 'experience':
            case 'motivation':
                return true; // Opcionales
            default:
                return false;
        }
    }

    // Mostrar mensaje con timeout automático
    function showMessage(messageElement, message, type, formElement = null) {
        messageElement.innerHTML = message;
        messageElement.className = `form_msg active ${type}`;
        
        if (type === 'success' && formElement) {
            setTimeout(() => {
                messageElement.classList.remove('active');
                formElement.reset();
                // Resetear labels
                formElement.querySelectorAll('.form_label').forEach(label => {
                    label.classList.remove('active');
                });
                // Resetear validaciones
                formElement.querySelectorAll('.form_input').forEach(input => {
                    input.classList.remove('valid', 'invalid');
                });
                // Resetear file display si existe
                resetFileDisplay();
            }, 3000);
        }
    }

    // Resetear display de archivo
    function resetFileDisplay() {
        const fileUploadDisplay = document.querySelector('.file_upload_display');
        const fileUploadText = document.querySelector('.file_upload_text');
        const fileName = document.getElementById('file_name');
        
        if (fileUploadDisplay && fileUploadText && fileName) {
            fileUploadDisplay.classList.remove('has_file');
            fileUploadText.textContent = '📄 Seleccionar archivo';
            fileName.textContent = '';
        }
    }

    // Función de validación en tiempo real común
    function setupFormValidation(form) {
        // Validación en tiempo real con clases CSS
        form.addEventListener('input', (e) => {
            if (e.target.matches('.form_input')) {
                const field = e.target.name;
                const value = e.target.value;
                const isValid = validateField(field, value);
                const label = e.target.nextElementSibling;
                
                // Remover clases anteriores
                e.target.classList.remove('valid', 'invalid');
                
                // Agregar clase según validación
                if (value.length > 0) {
                    e.target.classList.add(isValid ? 'valid' : 'invalid');
                }
                
                // Activar label
                if (label && label.classList.contains('form_label')) {
                    if (value.length > 0) {
                        label.classList.add('active');
                    } else {
                        label.classList.remove('active');
                    }
                }
            }
        });

        // Manejar blur para labels
        form.addEventListener('blur', (e) => {
            if (e.target.matches('.form_input')) {
                const label = e.target.nextElementSibling;
                if (label && label.classList.contains('form_label') && e.target.value.length === 0) {
                    label.classList.remove('active');
                }
            }
        }, true);

        // Manejar change para selects
        form.addEventListener('change', (e) => {
            if (e.target.matches('select.form_input')) {
                const label = e.target.nextElementSibling;
                e.target.classList.remove('valid', 'invalid');
                
                if (e.target.value) {
                    e.target.classList.add('valid');
                    if (label && label.classList.contains('form_label')) {
                        label.classList.add('active');
                    }
                }
            }
        });
    }

    // Configurar formulario de contacto
    if (contactForm && contactMsg) {
        setupFormValidation(contactForm);
        
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = contactForm.querySelector('.form_submit');
            
            // Deshabilitar botón y cambiar texto
            submitBtn.disabled = true;
            submitBtn.value = 'Enviando...';
            
            // Limpiar mensajes anteriores
            contactMsg.classList.remove('active');
            
            const formData = new FormData(contactForm);
            
            // Validación frontend
            const name = formData.get('name')?.trim();
            const number = formData.get('number')?.trim();
            const message = formData.get('message')?.trim();
            
            if (!validateField('name', name) || !validateField('number', number) || !validateField('message', message)) {
                showMessage(contactMsg, 'Por favor, complete todos los campos correctamente', 'error');
                submitBtn.disabled = false;
                submitBtn.value = 'Contactar';
                return;
            }

            try {
                const response = await fetch('./php/send_form_simple.php', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                
                switch(data) {
                    case 'empty':
                        showMessage(contactMsg, 'Complete todos los campos correctamente', 'error');
                        break;
                    case 'invalid_data':
                        showMessage(contactMsg, 'Los datos ingresados no son válidos', 'error');
                        break;
                    case 'invalid_phone':
                        showMessage(contactMsg, 'El número de teléfono no es válido', 'error');
                        break;
                    case 'rate_limit':
                        showMessage(contactMsg, 'Debe esperar antes de enviar otro mensaje', 'error');
                        break;
                    case 'success':
                        showMessage(contactMsg, '¡Mensaje enviado con éxito! Nos pondremos en contacto pronto.', 'success', contactForm);
                        break;
                    case 'error':
                    default:
                        showMessage(contactMsg, 'Ocurrió un error. Intente nuevamente o contáctenos por WhatsApp.', 'error');
                        break;
                }
            } catch (error) {
                console.error('Error:', error);
                showMessage(contactMsg, 'Error de conexión. Verifique su internet o contáctenos por WhatsApp.', 'error');
            } finally {
                // Rehabilitar botón
                submitBtn.disabled = false;
                submitBtn.value = 'Contactar';
            }
        });
    }

    // Configurar formulario de carreras
    if (careersForm && careersMsg) {
        setupFormValidation(careersForm);
        
        careersForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = careersForm.querySelector('.careers_submit');
            
            // Deshabilitar botón y cambiar texto
            submitBtn.disabled = true;
            submitBtn.value = 'Enviando...';
            
            // Limpiar mensajes anteriores
            careersMsg.classList.remove('active');
            
            const formData = new FormData(careersForm);
            
            // Validación frontend
            const fullName = formData.get('full_name')?.trim();
            const email = formData.get('email')?.trim();
            const phone = formData.get('phone')?.trim();
            const position = formData.get('position');
            
            if (!validateField('full_name', fullName) || !validateField('email', email) || 
                !validateField('phone', phone) || !validateField('position', position)) {
                showMessage(careersMsg, 'Por favor, complete todos los campos requeridos correctamente', 'error');
                submitBtn.disabled = false;
                submitBtn.value = 'Enviar Aplicación';
                return;
            }

            try {
                const response = await fetch('./php/send_form_simple.php', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                
                switch(data) {
                    case 'empty':
                        showMessage(careersMsg, 'Complete todos los campos requeridos', 'error');
                        break;
                    case 'invalid_data':
                        showMessage(careersMsg, 'Los datos ingresados no son válidos', 'error');
                        break;
                    case 'invalid_email':
                        showMessage(careersMsg, 'El email ingresado no es válido', 'error');
                        break;
                    case 'invalid_phone':
                        showMessage(careersMsg, 'El número de teléfono no es válido', 'error');
                        break;
                    case 'invalid_file_type':
                        showMessage(careersMsg, 'Solo se permiten archivos PDF, DOC o DOCX', 'error');
                        break;
                    case 'file_too_large':
                        showMessage(careersMsg, 'El archivo es demasiado grande. Máximo 5MB', 'error');
                        break;
                    case 'file_upload_error':
                        showMessage(careersMsg, 'Error al subir el archivo. Inténtalo nuevamente', 'error');
                        break;
                    case 'rate_limit':
                        showMessage(careersMsg, 'Debe esperar antes de enviar otra aplicación', 'error');
                        break;
                    case 'success':
                        showMessage(careersMsg, '¡Aplicación enviada con éxito! Revisaremos tu información y te contactaremos pronto.', 'success', careersForm);
                        break;
                    case 'error':
                    default:
                        showMessage(careersMsg, 'Ocurrió un error. Intente nuevamente o envíe su CV por email.', 'error');
                        break;
                }
            } catch (error) {
                console.error('Error:', error);
                showMessage(careersMsg, 'Error de conexión. Verifique su internet o envíe su CV por email.', 'error');
            } finally {
                // Rehabilitar botón
                submitBtn.disabled = false;
                submitBtn.value = 'Enviar Aplicación';
            }
        });
    }
})();