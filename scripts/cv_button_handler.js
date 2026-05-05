(function(){
    // Manejo del botón de envío de CV
    const cvButton = document.querySelector('.cv_upload_link');
    
    if (cvButton) {
        cvButton.addEventListener('click', function() {
            // Cambiar a estado de éxito (verde) inmediatamente cuando se hace clic
            this.classList.add('success');
            
            // Cambiar el texto del botón para mostrar que se está procesando
            const span = this.querySelector('span');
            const originalText = span.textContent;
            span.textContent = '✅ Abriendo cliente de correo...';
            
            // Después de 3 segundos, mostrar mensaje de éxito
            setTimeout(() => {
                span.textContent = '✅ CV enviado correctamente';
            }, 3000);
            
            // Después de 6 segundos, volver al estado original
            setTimeout(() => {
                this.classList.remove('success');
                span.textContent = originalText;
            }, 6000);
        });
    }
})();