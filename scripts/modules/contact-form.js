/* ContactForm — módulo ES
 * Lógica original de send_contact_form.js sin cambios. Solo envuelto en init() + export.
 * Selectores reales: #form, #form_msg, .btn-whatsapp-submit, .form_input, .form_label
 * Mantiene CSRF token, validación en tiempo real y manejo de estados del botón.
 */
const ContactForm = {
  init() {
    const form = document.getElementById('form');
    if (!form) return; // guard

    const form_msg = document.getElementById('form_msg');
    const submitBtn = form.querySelector('.btn-whatsapp-submit');
    const originalBtnHTML = submitBtn ? submitBtn.innerHTML : '';

    function validateField(field, value) {
      switch (field) {
        case 'name':    return value.trim().length >= 2;
        case 'number':  return /^[\d\s\+\-\(\)]{7,}$/.test(value.trim());
        case 'message': return value.trim().length >= 10;
        default:        return false;
      }
    }

    function showMessage(message, type) {
      if (!form_msg) return;
      form_msg.innerHTML = message;
      form_msg.className = `form_msg active ${type}`;
      if (type === 'success') {
        setTimeout(() => {
          form_msg.classList.remove('active');
          form.reset();
          document.querySelectorAll('.form_label').forEach(label => {
            label.classList.remove('active');
          });
        }, 3000);
      }
    }

    // Validación en tiempo real
    form.addEventListener('input', (e) => {
      if (!e.target.matches('.form_input')) return;
      const field = e.target.name;
      const value = e.target.value;
      const isValid = validateField(field, value);
      const label = e.target.nextElementSibling;

      e.target.classList.remove('valid', 'invalid');
      if (value.length > 0) e.target.classList.add(isValid ? 'valid' : 'invalid');

      if (label && label.classList.contains('form_label')) {
        if (value.length > 0 || e.target === document.activeElement) {
          label.classList.add('active');
        } else {
          label.classList.remove('active');
        }
      }
    });

    form.addEventListener('focus', (e) => {
      if (!e.target.matches('.form_input')) return;
      const label = e.target.nextElementSibling;
      if (label && label.classList.contains('form_label')) label.classList.add('active');
    }, true);

    form.addEventListener('blur', (e) => {
      if (!e.target.matches('.form_input')) return;
      const label = e.target.nextElementSibling;
      if (label && label.classList.contains('form_label') && e.target.value.length === 0) {
        label.classList.remove('active');
      }
    }, true);

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

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Enviando...';
      }

      const formData = new FormData(form);
      const csrfToken = await getCsrfToken();

      if (!csrfToken) {
        showMessage('Error de seguridad. Intente más tarde.', 'error');
        if (submitBtn) { submitBtn.disabled = false; submitBtn.innerHTML = originalBtnHTML; }
        return;
      }

      formData.append('csrf_token', csrfToken);

      const name    = formData.get('name')?.trim();
      const number  = formData.get('number')?.trim();
      const message = formData.get('message')?.trim();

      let hasError = false;
      if (!validateField('name', name)) {
        form.querySelector('[name="name"]').classList.add('invalid');
        hasError = true;
      }
      if (!validateField('number', number)) {
        form.querySelector('[name="number"]').classList.add('invalid');
        hasError = true;
      }
      if (!validateField('message', message)) {
        form.querySelector('[name="message"]').classList.add('invalid');
        hasError = true;
      }

      if (hasError) {
        showMessage('Por favor, revise los campos marcados en rojo', 'error');
        if (submitBtn) { submitBtn.disabled = false; submitBtn.innerHTML = originalBtnHTML; }
        return;
      }

      try {
        const response = await fetch('./php/send_form.php', { method: 'POST', body: formData });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        switch (data) {
          case 'empty':
            showMessage('Complete todos los campos correctamente', 'error');
            break;
          case 'success':
            showMessage('¡Mensaje enviado con éxito! Nos pondremos en contacto pronto.', 'success');
            break;
          default:
            showMessage('Ocurrió un error. Intente nuevamente o contáctenos por WhatsApp.', 'error');
        }
      } catch (error) {
        console.error('Error:', error);
        showMessage('Error de conexión. Verifique su internet o contáctenos por WhatsApp.', 'error');
      } finally {
        if (submitBtn) { submitBtn.disabled = false; submitBtn.innerHTML = originalBtnHTML; }
      }
    });
  },
};

export default ContactForm;
