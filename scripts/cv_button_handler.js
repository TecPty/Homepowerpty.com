(function(){
    // Manejo del botón de envío de CV
    const cvButton = document.querySelector('.cv_upload_link');
    
    if (cvButton) {
        cvButton.addEventListener('click', function() {
            this.classList.add('success');            
            const span = this.querySelector('span');
            const originalText = span.textContent;
            span.textContent = ' Abriendo cliente de correo...';
                        setTimeout(() => {
                span.textContent = ' CV enviado correctamente';
            }, 3000);
                        setTimeout(() => {
                this.classList.remove('success');
                span.textContent = originalText;
            }, 6000);
        });
    }
})();