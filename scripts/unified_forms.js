/**
 * SCRIPT UNIFICADO - Formularios de Contacto y Carreras
 * Maneja ambos formularios + carga de archivos sin conflictos
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 UNIFIED SCRIPT: Iniciando...');
    
    // ======================
    // CONFIGURACIÓN DE ARCHIVO
    // ======================
    setupFileUpload();
    
    // ======================
    // FORMULARIO DE CONTACTO
    // ======================
    const contactForm = document.getElementById('form');
    if (contactForm) {
        console.log('✅ Formulario de contacto encontrado');
        contactForm.addEventListener('submit', handleContactSubmit);
        setupFormValidation(contactForm);
    }
    
    // ======================
    // FORMULARIO DE CARRERAS
    // ======================
    const careersForm = document.getElementById('careers_form');
    if (careersForm) {
        console.log('✅ Formulario de carreras encontrado');
        careersForm.addEventListener('submit', handleCareersSubmit);
        setupFormValidation(careersForm);
    }
    
    console.log('🎯 UNIFIED SCRIPT: Todo configurado');
});

// ======================
// CONFIGURACIÓN ARCHIVO
// ======================
function setupFileUpload() {
    const fileInput = document.getElementById('cv_file');
    const fileUploadDisplay = document.querySelector('.file_upload_display');
    const fileUploadText = document.querySelector('.file_upload_text');
    const fileName = document.getElementById('file_name');
    
    if (!fileInput || !fileUploadDisplay) {
        console.log('⚠️ Elementos de archivo no encontrados');
        return;
    }
    
    console.log('📁 Configurando carga de archivos...');
    
    // Click para activar input
    fileUploadDisplay.addEventListener('click', function() {
        console.log('📂 Click en área de archivo');
        fileInput.click();
    });
    
    // Cambio de archivo
    fileInput.addEventListener('change', function() {
        console.log('📄 Archivo seleccionado');
        const file = this.files[0];
        
        if (file) {
            console.log('📋 Archivo:', file.name, file.size, file.type);
            
            // Validar tipo
            const allowedTypes = [
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            ];
            
            if (!allowedTypes.includes(file.type)) {
                alert('Solo se permiten archivos PDF, DOC o DOCX');
                this.value = '';
                resetFileDisplay();
                return;
            }
            
            // Validar tamaño (5MB)
            if (file.size > 5 * 1024 * 1024) {
                alert('Archivo muy grande. Máximo 5MB');
                this.value = '';
                resetFileDisplay();
                return;
            }
            
            // Mostrar archivo
            if (fileUploadDisplay && fileUploadText && fileName) {
                fileUploadDisplay.classList.add('has_file');
                fileUploadText.textContent = '✓ Archivo seleccionado';
                fileName.textContent = file.name;
                console.log('✅ Archivo válido mostrado');
            }
        } else {
            resetFileDisplay();
        }
    });
    
    console.log('✅ Carga de archivos configurada');
}

function resetFileDisplay() {
    const fileUploadDisplay = document.querySelector('.file_upload_display');
    const fileUploadText = document.querySelector('.file_upload_text');
    const fileName = document.getElementById('file_name');
    
    if (fileUploadDisplay) fileUploadDisplay.classList.remove('has_file');
    if (fileUploadText) fileUploadText.textContent = '📄 Seleccionar archivo';
    if (fileName) fileName.textContent = '';
}

// ======================
// MANEJO FORMULARIO CONTACTO
// ======================
async function handleContactSubmit(e) {
    e.preventDefault();
    console.log('📧 Enviando formulario de contacto');
    
    const form = e.target;
    const submitBtn = form.querySelector('.form_submit');
    const messageDiv = document.getElementById('form_msg');
    
    if (!validateContactForm(form)) {
        console.log('❌ Validación falló');
        return;
    }
    
    const originalText = submitBtn.value;
    submitBtn.disabled = true;
    submitBtn.value = 'Enviando...';
    
    try {
        const formData = new FormData(form);
        console.log('📤 Enviando a php/test_form.php');
        
        const response = await fetch('php/test_form.php', {
            method: 'POST',
            body: formData
        });
        
        console.log('📡 Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        console.log('✅ Respuesta:', data);
        
        handleResponse(data, messageDiv, 'contacto');
        
        if (data === 'success') {
            form.reset();
            removeValidationClasses(form);
        }
        
    } catch (error) {
        console.error('❌ Error:', error);
        showMessage(messageDiv, 'Error de conexión. Intenta nuevamente.', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.value = originalText;
    }
}

// ======================
// MANEJO FORMULARIO CARRERAS
// ======================
async function handleCareersSubmit(e) {
    e.preventDefault();
    console.log('💼 Enviando formulario de carreras');
    
    const form = e.target;
    const submitBtn = form.querySelector('.careers_submit');
    const messageDiv = document.getElementById('careers_form_msg');
    
    if (!validateCareersForm(form)) {
        console.log('❌ Validación carreras falló');
        return;
    }
    
    const originalText = submitBtn.value;
    submitBtn.disabled = true;
    submitBtn.value = 'Enviando...';
    
    try {
        const formData = new FormData(form);
        console.log('📤 Enviando carreras a php/test_form.php');
        
        // Debug FormData
        for (let [key, value] of formData.entries()) {
            console.log(`📋 ${key}:`, value);
        }
        
        const response = await fetch('php/test_form.php', {
            method: 'POST',
            body: formData
        });
        
        console.log('📡 Carreras response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        console.log('✅ Carreras respuesta:', data);
        
        handleResponse(data, messageDiv, 'aplicación');
        
        if (data === 'success') {
            form.reset();
            removeValidationClasses(form);
            resetFileDisplay();
        }
        
    } catch (error) {
        console.error('❌ Carreras error:', error);
        showMessage(messageDiv, 'Error de conexión. Intenta nuevamente.', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.value = originalText;
    }
}

// ======================
// VALIDACIONES
// ======================
function validateContactForm(form) {
    const name = form.querySelector('[name="name"]').value.trim();
    const number = form.querySelector('[name="number"]').value.trim();
    const message = form.querySelector('[name="message"]').value.trim();
    
    if (!name || name.length < 2) return false;
    if (!number || !/^[\d\s\+\-\(\)]{7,}$/.test(number)) return false;
    if (!message || message.length < 10) return false;
    
    return true;
}

function validateCareersForm(form) {
    const fullName = form.querySelector('[name="full_name"]').value.trim();
    const email = form.querySelector('[name="email"]').value.trim();
    const phone = form.querySelector('[name="phone"]').value.trim();
    const position = form.querySelector('[name="position"]').value;
    
    if (!fullName || fullName.length < 3) return false;
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return false;
    if (!phone || !/^[\d\s\+\-\(\)]{7,}$/.test(phone)) return false;
    if (!position) return false;
    
    return true;
}

// ======================
// RESPUESTAS Y MENSAJES
// ======================
function handleResponse(response, messageDiv, formType) {
    const messages = {
        'success': `¡Tu ${formType} ha sido enviado exitosamente! Te contactaremos pronto.`,
        'empty': 'Complete todos los campos requeridos.',
        'invalid_data': 'Datos no válidos.',
        'invalid_phone': 'Número de teléfono no válido.',
        'invalid_email': 'Email no válido.',
        'invalid_file_type': 'Solo archivos PDF, DOC, DOCX.',
        'file_too_large': 'Archivo muy grande (máx 5MB).',
        'file_upload_error': 'Error subiendo archivo.',
        'rate_limit': 'Espera antes de enviar otro mensaje.',
        'error': 'Error al enviar. Intenta nuevamente.'
    };
    
    const message = messages[response] || messages['error'];
    const type = response === 'success' ? 'success' : 'error';
    
    showMessage(messageDiv, message, type);
}

function showMessage(messageDiv, text, type) {
    if (messageDiv) {
        messageDiv.textContent = text;
        messageDiv.className = `form_msg ${type} active`;
        
        setTimeout(() => {
            messageDiv.classList.remove('active');
        }, 5000);
    }
}

// ======================
// VALIDACIÓN EN TIEMPO REAL
// ======================
function setupFormValidation(form) {
    const inputs = form.querySelectorAll('.form_input');
    
    inputs.forEach(input => {
        const label = input.nextElementSibling;
        
        // Labels flotantes
        input.addEventListener('focus', function() {
            if (label && label.classList.contains('form_label')) {
                label.classList.add('active');
            }
        });
        
        input.addEventListener('blur', function() {
            if (label && label.classList.contains('form_label') && !this.value) {
                label.classList.remove('active');
            }
        });
        
        input.addEventListener('input', function() {
            if (label && label.classList.contains('form_label')) {
                if (this.value) {
                    label.classList.add('active');
                } else {
                    label.classList.remove('active');
                }
            }
        });
    });
}

function removeValidationClasses(form) {
    const inputs = form.querySelectorAll('.form_input');
    inputs.forEach(input => {
        input.classList.remove('valid', 'invalid');
    });
    
    const labels = form.querySelectorAll('.form_label');
    labels.forEach(label => {
        label.classList.remove('active');
    });
}