(function(){
    const header = document.getElementById('header'),
    section_clients = document.getElementById('section_clients'),
    btn_menu = document.getElementById('btn_menu'),
    btn_menu_close = document.getElementById('btn_menu_close'),
    menu_item = document.querySelectorAll('.menu_item'),
    overlay = document.getElementById('overlay')


    for (let i = 0; i < menu_item.length; i++) {
        menu_item[i].addEventListener('click', () => {
            header.classList.remove('translate')
            overlay.classList.remove('active')
        })
    }

    btn_menu.addEventListener('click', () => {
        header.classList.add('translate')
        overlay.classList.add('active')
    })

    btn_menu_close.addEventListener('click', () => {
        header.classList.remove('translate')
        overlay.classList.remove('active')
    })

    overlay.addEventListener('click', () => {
        header.classList.remove('translate')
        overlay.classList.remove('active')
    })

    window.addEventListener('scroll', () => {
        let scroll_y = window.scrollY
        header.classList.toggle('active', scroll_y > 40)
        
        section_clients_top = section_clients.getBoundingClientRect().top
        if (section_clients_top + 600 <= window.innerHeight) {
            header.classList.add('background')
        } else {
            header.classList.remove('background')
        }
    })

}())