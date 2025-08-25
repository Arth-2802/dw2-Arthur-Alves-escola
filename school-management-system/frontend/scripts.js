// Funções utilitárias para acessibilidade e feedback
function showModal(id) {
  document.getElementById(id).hidden = false;
  document.getElementById(id).querySelector('input, select, button').focus();
}
function hideModal(id) {
  document.getElementById(id).hidden = true;
}

// Eventos para abrir/fechar modais
document.getElementById('btnNovoAluno').addEventListener('click', () => showModal('modalAluno'));
document.getElementById('fecharModalAluno').addEventListener('click', () => hideModal('modalAluno'));
document.getElementById('btnNovaMatricula').addEventListener('click', () => showModal('modalMatricula'));
document.getElementById('fecharModalMatricula').addEventListener('click', () => hideModal('modalMatricula'));

// Exemplo de validação de idade mínima (5 anos)
document.getElementById('formAluno').addEventListener('submit', function(e) {
  e.preventDefault();
  const nome = this.nome.value.trim();
  const data_nascimento = new Date(this.data_nascimento.value);
  const email = this.email.value.trim();
  const status = this.status.value;
  const hoje = new Date();
  const idade = hoje.getFullYear() - data_nascimento.getFullYear();
  const feedback = document.getElementById('feedbackAluno');
  feedback.textContent = '';

  if (nome.length < 3 || nome.length > 80) {
    feedback.textContent = 'Nome deve ter entre 3 e 80 caracteres.';
    this.nome.focus();
    return;
  }
  if (isNaN(data_nascimento.getTime()) || idade < 5 || (hoje - data_nascimento) < (5 * 365 * 24 * 60 * 60 * 1000)) {
    feedback.textContent = 'Aluno deve ter pelo menos 5 anos.';
    this.data_nascimento.focus();
    return;
  }
  if (email && !/^[^@]+@[^@]+\.[^@]+$/.test(email)) {
    feedback.textContent = 'Email inválido.';
    this.email.focus();
    return;
  }
  if (!['ativo', 'inativo'].includes(status)) {
    feedback.textContent = 'Status inválido.';
    this.status.focus();
    return;
  }
  // Aqui você pode chamar a função para enviar os dados via fetch para a API
  feedback.textContent = 'Salvando...';
  // ...enviar dados...
});
