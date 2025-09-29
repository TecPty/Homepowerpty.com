(function(){
    const form = document.getElementById('form'),
          form_msg = document.getElementById('form_msg'),
          submitBtn = form.querySelector('.form_submit');

    // Validación en tiempo real
    function validateField(field, value) {
        switch(field) {
            case 'name':
                return value.trim().length >= 2;
            case 'number':
                return /^[\d\s\+\-\(\)]{7,}$/.test(value.trim());
            case 'message':
                return value.trim().length >= 10;
            default:
                return false;
        }
    }

    // Mostrar mensaje con timeout automático
    function showMessage(message, type) {
        form_msg.innerHTML = message;
        form_msg.className = `form_msg active ${type}`;
        
        if (type === 'success') {
            setTimeout(() => {
                form_msg.classList.remove('active');
                form.reset();
                // Resetear labels
                document.querySelectorAll('.form_label').forEach(label => {
                    label.classList.remove('active');
                });
            }, 3000);
        }
    }

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

    // Envío del formulario
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Deshabilitar botón y cambiar texto
        submitBtn.disabled = true;
        submitBtn.value = 'Enviando...';
        
        // Limpiar mensajes anteriores
        form_msg.classList.remove('active');
        
        const formData = new FormData(form);
        
        // Validación frontend
        const name = formData.get('name')?.trim();
        const number = formData.get('number')?.trim();
        const message = formData.get('message')?.trim();
        
        if (!validateField('name', name) || !validateField('number', number) || !validateField('message', message)) {
            showMessage('Por favor, complete todos los campos correctamente', 'error');
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
                    showMessage('Complete todos los campos correctamente', 'error');
                    break;
                case 'invalid_data':
                    showMessage('Los datos ingresados no son válidos', 'error');
                    break;
                case 'invalid_phone':
                    showMessage('El número de teléfono no es válido', 'error');
                    break;
                case 'rate_limit':
                    showMessage('Debe esperar antes de enviar otro mensaje', 'error');
                    break;
                case 'success':
                    showMessage('¡Mensaje enviado con éxito! Nos pondremos en contacto pronto.', 'success');
                    break;
                case 'error':
                default:
                    showMessage('Ocurrió un error. Intente nuevamente o contáctenos por WhatsApp.', 'error');
                    break;
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('Error de conexión. Verifique su internet o contáctenos por WhatsApp.', 'error');
        } finally {
            // Rehabilitar botón
            submitBtn.disabled = false;
            submitBtn.value = 'Contactar';
        }
    });
})();