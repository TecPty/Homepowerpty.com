(function(){
    const form = document.getElementById('careers_form'),
          form_msg = document.getElementById('careers_form_msg'),
          submitBtn = form.querySelector('.careers_submit');

    // Validación en tiempo real para formulario de carreras
    function validateField(field, value) {
        switch(field) {
            case 'full_name':
                return value.trim().length >= 2;
            case 'email':
                return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
            case 'phone':
                return /^[\d\s\+\-\(\)]{7,}$/.test(value.trim());
            case 'position':
                return value.trim().length > 0;
            case 'experience':
                return value.trim().length >= 5;
            case 'motivation':
                return value.trim().length >= 20;
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
                document.querySelectorAll('#careers_form .form_label').forEach(label => {
                    label.classList.remove('active');
                });
                // Resetear select
                const selectInput = form.querySelector('.form_select');
                if (selectInput) {
                    selectInput.selectedIndex = 0;
                }
            }, 5000);
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
            
            // Manejar label activo para inputs y textareas
            if (label && label.classList.contains('form_label')) {
                if (value.length > 0 || e.target === document.activeElement) {
                    label.classList.add('active');
                } else {
                    label.classList.remove('active');
                }
            }
        }
    });

    // Manejar cambios en select
    form.addEventListener('change', (e) => {
        if (e.target.matches('.form_select')) {
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
            
            // Manejar label activo para select
            if (label && label.classList.contains('form_label')) {
                if (value.length > 0) {
                    label.classList.add('active');
                } else {
                    label.classList.remove('active');
                }
            }
        }
    });

    // Manejar focus para labels
    form.addEventListener('focus', (e) => {
        if (e.target.matches('.form_input')) {
            const label = e.target.nextElementSibling;
            if (label && label.classList.contains('form_label')) {
                label.classList.add('active');
            }
        }
    }, true);

    // Manejar blur para labels
    form.addEventListener('blur', (e) => {
        if (e.target.matches('.form_input')) {
            const label = e.target.nextElementSibling;
            if (label && label.classList.contains('form_label') && 
                e.target.value.length === 0 && !e.target.matches('.form_select')) {
                label.classList.remove('active');
            }
        }
    }, true);

    // Agregar token CSRF
    async function getCsrfToken() {
        try {
            const response = await fetch('./php/get_csrf_token.php');
            const data = await response.json();
            return data.token;
        } catch (error) {
            console.error('Error obteniendo CSRF token:', error);
            return null;
        }
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Deshabilitar botón durante envío
        submitBtn.disabled = true;
        submitBtn.value = 'Enviando...';
        
        const formData = new FormData(form);
        const cvInput = document.getElementById('cv_file');
        if (cvInput && cvInput.files && cvInput.files.length > 0) {
            formData.append('cv_file', cvInput.files[0]);
        }
        const csrfToken = await getCsrfToken();
        
        if (!csrfToken) {
            showMessage('Error de seguridad. Intente más tarde.', 'error');
            submitBtn.disabled = false;
            submitBtn.value = 'Enviar Aplicación';
            return;
        }
        
        formData.append('csrf_token', csrfToken);
        
        // Validación frontend
        const full_name = formData.get('full_name')?.trim();
        const email = formData.get('email')?.trim();
        const phone = formData.get('phone')?.trim();
        const position = formData.get('position')?.trim();
        const experience = formData.get('experience')?.trim();
        const motivation = formData.get('motivation')?.trim();
        
        // Validar todos los campos
        if (!validateField('full_name', full_name) || 
            !validateField('email', email) || 
            !validateField('phone', phone) || 
            !validateField('position', position) ||
            !validateField('motivation', motivation)) {
            showMessage('Por favor, complete todos los campos correctamente. La motivación debe tener al menos 20 caracteres.', 'error');
            submitBtn.disabled = false;
            submitBtn.value = 'Enviar Aplicación';
            return;
        }

        try {
            const response = await fetch('./php/send_form.php', {
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
                case 'invalid':
                    showMessage('Algunos datos no son válidos. Verifique su email y que la motivación tenga al menos 20 caracteres.', 'error');
                    break;
                case 'success':\n                    showMessage('Aplicación enviada con éxito. CV recibido, nos contactaremos…', 'success');\n                    break;
                case 'error':
                default:
                    showMessage('Ocurrió un error. Intente nuevamente o contáctenos directamente.', 'error');
                    break;
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('Error de conexión. Verifique su internet e intente nuevamente.', 'error');
        } finally {
            // Rehabilitar botón
            submitBtn.disabled = false;
            submitBtn.value = 'Enviar Aplicación';
        }
    });
})();

