(function () {
  const form = document.getElementById('careers_form');
  if (!form) return;

  const formMsg = document.getElementById('careers_form_msg');
  const submitBtn = form.querySelector('.careers_submit');
  const cvInput = document.getElementById('cv_file');
  const cvTrigger = document.getElementById('cv_trigger');
  const fileName = document.getElementById('file_name');

  function validateField(field, value) {
    switch (field) {
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
      default:
        return false;
    }
  }

  function showMessage(message, type) {
    if (!formMsg) return;
    formMsg.innerHTML = message;
    formMsg.className = `form_msg active ${type}`;
    if (type === 'success') {
      setTimeout(() => formMsg.classList.remove('active'), 4000);
    }
  }

  // Autofocus label behavior
  form.addEventListener(
    'input',
    (e) => {
      if (!e.target.matches('.form_input')) return;
      const field = e.target.name;
      const value = e.target.value;
      const isValid = validateField(field, value);
      e.target.classList.remove('valid', 'invalid');
      if (value.length > 0) e.target.classList.add(isValid ? 'valid' : 'invalid');
      const label = e.target.nextElementSibling;
      if (label && label.classList.contains('form_label')) {
        if (value.length > 0 || e.target === document.activeElement) {
          label.classList.add('active');
        } else {
          label.classList.remove('active');
        }
      }
    },
    true
  );

  // Trigger file select
  if (cvTrigger && cvInput) {
    cvTrigger.addEventListener('click', () => cvInput.click());
    cvInput.addEventListener('change', () => {
      const file = cvInput.files && cvInput.files[0];
      if (fileName) fileName.textContent = file ? file.name : 'Ningún archivo seleccionado';
    });
  }

  async function getCsrfToken() {
    try {
      const response = await fetch('./php/get_csrf_token.php');
      const data = await response.json();
      return data.token;
    } catch (err) {
      console.error('CSRF error', err);
      return null;
    }
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.value = 'Enviando...';
    }

    const formData = new FormData(form);
    if (cvInput && cvInput.files && cvInput.files.length > 0) {
      formData.append('cv_file', cvInput.files[0]);
    }

    const csrfToken = await getCsrfToken();
    if (!csrfToken) {
      showMessage('Error de seguridad. Intente más tarde.', 'error');
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.value = 'Enviar Aplicación';
      }
      return;
    }
    formData.append('csrf_token', csrfToken);

    const full_name = formData.get('full_name')?.trim() || '';
    const email = formData.get('email')?.trim() || '';
    const phone = formData.get('phone')?.trim() || '';
    const position = formData.get('position')?.trim() || '';
    const experience = formData.get('experience')?.trim() || '';

    if (
      !validateField('full_name', full_name) ||
      !validateField('email', email) ||
      !validateField('phone', phone) ||
      !validateField('position', position) ||
      !validateField('experience', experience)
    ) {
      showMessage('Por favor, complete todos los campos correctamente.', 'error');
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.value = 'Enviar Aplicación';
      }
      return;
    }

    try {
      const res = await fetch('./php/send_form.php', { method: 'POST', body: formData });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      if (data === 'success') {
        showMessage('Aplicación enviada con éxito. CV recibido.', 'success');
        form.reset();
        if (fileName) fileName.textContent = 'Ningún archivo seleccionado';
      } else if (data === 'invalid') {
        showMessage('Datos inválidos. Verifique los campos.', 'error');
      } else if (data === 'empty') {
        showMessage('Complete todos los campos correctamente.', 'error');
      } else {
        showMessage('Ocurrió un error. Intente nuevamente.', 'error');
      }
    } catch (err) {
      console.error(err);
      showMessage('Error de conexión. Intente nuevamente.', 'error');
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.value = 'Enviar Aplicación';
      }
    }
  });
})();
