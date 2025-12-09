// Código para o Menu Lateral
    const menuIcon = document.querySelector('.menu-icon');
    const sidebarMenu = document.getElementById('sidebar-menu');

    // Função para alternar o estado do menu (abrir/fechar)
    function toggleMenu() {
        sidebarMenu.classList.toggle('active');
        // Você pode adicionar um overlay se desejar aqui
    }

    // Evento de clique no ícone do menu
    if (menuIcon) {
        menuIcon.addEventListener('click', toggleMenu);
    }