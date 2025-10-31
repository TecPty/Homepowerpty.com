document.addEventListener('DOMContentLoaded', function(){
  const input = document.getElementById('cv_file');
  const btn = document.getElementById('cv_button');
  const fileNameEl = document.getElementById('file_name');
  const msg = document.getElementById('careers_form_msg');

  function showMsg(text, type){
    if (!msg) return;
    msg.textContent = text;
    msg.className = 'form_msg ' + type + ' active';
    setTimeout(()=>{ msg.classList.remove('active'); }, 5000);
  }

  if (btn && input){
    btn.addEventListener('click', function(){ input.click(); });
  }

  if (input){
    input.addEventListener('change', function(){
      const file = this.files && this.files[0];
      if (!file){
        if (fileNameEl) fileNameEl.textContent = 'Ningún archivo seleccionado';
        return;
      }
      const allowed = ['application/pdf','application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      const isAllowed = allowed.includes(file.type) || /\.(pdf|doc|docx)$/i.test(file.name);
      if (!isAllowed){
        this.value = '';
        if (fileNameEl) fileNameEl.textContent = 'Ningún archivo seleccionado';
        showMsg('Formato no permitido. Adjunta PDF, DOC o DOCX.', 'error');
        return;
      }
      const max = 5 * 1024 * 1024; // 5MB
      if (file.size > max){
        this.value = '';
        if (fileNameEl) fileNameEl.textContent = 'Ningún archivo seleccionado';
        showMsg('El archivo supera 5MB. Reduce el tamaño e intenta de nuevo.', 'error');
        return;
      }
      if (fileNameEl) fileNameEl.textContent = file.name;
    });
  }
});

