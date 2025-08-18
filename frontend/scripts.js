// scripts.js - JS principal do sistema de gestão escolar
// Tema claro/escuro com persistência
(function() {
    const temaSalvo = localStorage.getItem('tema') || 'claro';
    document.documentElement.setAttribute('data-tema', temaSalvo);
    window.toggleTema = function() {
        const atual = document.documentElement.getAttribute('data-tema');
        const novo = atual === 'claro' ? 'escuro' : 'claro';
        document.documentElement.setAttribute('data-tema', novo);
        localStorage.setItem('tema', novo);
    };
})();
// ...outros scripts virão aqui...
