/**
 * DEBUG: Formulario de carreras simplificado
 * Versión para identificar el problema
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔍 DEBUG: Script cargado');
    
    const careersForm = document.getElementById('careers_form');
    const careersMsg = document.getElementById('careers_form_msg');
    
    if (!careersForm) {
        console.error('❌ DEBUG: No se encontró el formulario careers_form');
        return;
    }
    
    if (!careersMsg) {
        console.error('❌ DEBUG: No se encontró careers_form_msg');
        return;
    }
    
    console.log('✅ DEBUG: Formulario y mensaje encontrados');
    
    // Función para mostrar mensajes
    function showMessage(message, type) {
        console.log(`📧 DEBUG: Mostrando mensaje: ${message} (${type})`);
        careersMsg.textContent = message;
        careersMsg.className = `form_msg ${type} active`;
        
        setTimeout(() => {
            careersMsg.classList.remove('active');
        }, 10000); // 10 segundos para debug
    }
    
    // Validación simple
    function validateForm() {
        const fullName = careersForm.querySelector('[name="full_name"]').value.trim();
        const email = careersForm.querySelector('[name="email"]').value.trim();
        const phone = careersForm.querySelector('[name="phone"]').value.trim();
        const position = careersForm.querySelector('[name="position"]').value;
        
        console.log('🔍 DEBUG: Valores del formulario:', {fullName, email, phone, position});
        
        if (!fullName || !email || !phone || !position) {
            showMessage('Complete todos los campos requeridos', 'error');
            return false;
        }
        
        // Validar email básico
        if (!email.includes('@') || !email.includes('.')) {
            showMessage('Email no válido', 'error');
            return false;
        }
        
        return true;
    }
    
    // Manejar envío del formulario
    careersForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        console.log('🚀 DEBUG: Formulario enviado');
        
        if (!validateForm()) {
            console.log('❌ DEBUG: Validación falló');
            return;
        }
        
        const submitBtn = careersForm.querySelector('.careers_submit');
        const originalText = submitBtn.value;
        
        try {
            submitBtn.disabled = true;
            submitBtn.value = 'Enviando...';
            console.log('📤 DEBUG: Preparando FormData...');
            
            const formData = new FormData(careersForm);
            
            // Debug: mostrar datos que se envían
            for (let [key, value] of formData.entries()) {
                console.log(`📋 DEBUG: ${key}: ${value}`);
            }
            
            console.log('🌐 DEBUG: Enviando request a php/send_form_simple.php');
            
            const response = await fetch('php/send_form_simple.php', {
                method: 'POST',
                body: formData
            });
            
            console.log('📡 DEBUG: Response status:', response.status);
            console.log('📡 DEBUG: Response ok:', response.ok);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const responseText = await response.text();
            console.log('📄 DEBUG: Response text:', responseText);
            
            let data;
            try {
                data = JSON.parse(responseText);
                console.log('✅ DEBUG: JSON parseado:', data);
            } catch (parseError) {
                console.error('❌ DEBUG: Error parsing JSON:', parseError);
                console.error('📄 DEBUG: Raw response:', responseText);
                throw new Error('Respuesta no válida del servidor');
            }
            
            // Manejar respuesta
            switch(data) {
                case 'success':
                    showMessage('¡Aplicación enviada con éxito! Te contactaremos pronto.', 'success');
                    careersForm.reset();
                    break;
                case 'empty':
                    showMessage('Complete todos los campos requeridos', 'error');
                    break;
                case 'invalid_email':
                    showMessage('Email no válido', 'error');
                    break;
                case 'invalid_file_type':
                    showMessage('Solo archivos PDF, DOC, DOCX', 'error');
                    break;
                case 'file_too_large':
                    showMessage('Archivo muy grande (máx 5MB)', 'error');
                    break;
                default:
                    showMessage('Error: ' + data, 'error');
                    break;
            }
            
        } catch (error) {
            console.error('❌ DEBUG: Error completo:', error);
            showMessage(`Error de conexión: ${error.message}`, 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.value = originalText;
            console.log('🔄 DEBUG: Formulario restaurado');
        }
    });
    
    console.log('✅ DEBUG: Event listeners configurados');
});