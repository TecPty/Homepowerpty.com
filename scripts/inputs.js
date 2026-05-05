(function(){
    const inputs = document.querySelectorAll('.form_input'),
    labels = document.querySelectorAll('.form_label')

    for (let i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener('input', () => {
            if(inputs[i].value.length > 1) {
                labels[i].classList.add('active')
            } else {
                labels[i].classList.remove('active')
            }
        })
        
    }
}())