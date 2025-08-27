// Configurações da API
const API_URL = 'http://localhost:8000';

// Cache de dados
let currentSection = 'alunos';
let alunosList = [];
let turmasList = [];

// Elementos do DOM
const sections = document.querySelectorAll('.section');
const navButtons = document.querySelectorAll('.nav-button');
const alunoModal = document.getElementById('alunoModal');
const turmaModal = document.getElementById('turmaModal');
const alunoForm = document.getElementById('alunoForm');
const turmaForm = document.getElementById('turmaForm');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    loadInitialData();
    setupEventListeners();
});

function setupEventListeners() {
    // Navegação
    navButtons.forEach(button => {
        button.addEventListener('click', () => switchSection(button.dataset.section));
    });

    // Filtros
    document.getElementById('filtroTurma').addEventListener('change', filterAlunos);
    document.getElementById('filtroStatus').addEventListener('change', filterAlunos);
    document.getElementById('busca').addEventListener('input', filterAlunos);

    // Modais
    document.getElementById('novoAluno').addEventListener('click', () => openAlunoModal());
    document.getElementById('novaTurma').addEventListener('click', () => openTurmaModal());
    
    // Formulários
    alunoForm.addEventListener('submit', handleAlunoSubmit);
    turmaForm.addEventListener('submit', handleTurmaSubmit);
    
    // Botões de fechar modal
    document.querySelectorAll('.close-modal').forEach(button => {
        button.addEventListener('click', () => {
            alunoModal.close();
            turmaModal.close();
        });
    });

    // Exportação
    document.getElementById('exportarAlunosCSV').addEventListener('click', () => exportarAlunos('csv'));
    document.getElementById('exportarAlunosJSON').addEventListener('click', () => exportarAlunos('json'));
}

// Funções de carregamento de dados
async function loadInitialData() {
    try {
        await Promise.all([loadTurmas(), loadAlunos()]);
        updateStats();
    } catch (error) {
        showError('Erro ao carregar dados iniciais');
        console.error(error);
    }
}

async function loadTurmas() {
    const response = await fetch(`${API_URL}/turmas`);
    turmasList = await response.json();
    updateTurmasTable();
    updateTurmasSelect();
}

async function loadAlunos() {
    const response = await fetch(`${API_URL}/alunos`);
    alunosList = await response.json();
    updateAlunosTable();
}

// Funções de atualização da UI
function switchSection(sectionId) {
    currentSection = sectionId;
    sections.forEach(section => {
        section.classList.toggle('active', section.id === sectionId);
    });
    navButtons.forEach(button => {
        button.classList.toggle('active', button.dataset.section === sectionId);
    });
}

function updateTurmasTable() {
    const tbody = document.getElementById('turmasLista');
    tbody.innerHTML = turmasList.map(turma => `
        <tr>
            <td>${escapeHtml(turma.nome)}</td>
            <td>${turma.capacidade}</td>
            <td>${turma.ocupacao} / ${turma.capacidade}</td>
            <td>
                <button onclick="deleteTurma(${turma.id})" 
                        aria-label="Deletar turma ${turma.nome}">
                    Deletar
                </button>
            </td>
        </tr>
    `).join('');
}

function updateAlunosTable(filteredAlunos = alunosList) {
    const tbody = document.getElementById('alunosLista');
    tbody.innerHTML = filteredAlunos.map(aluno => `
        <tr>
            <td>${escapeHtml(aluno.nome)}</td>
            <td>${formatDate(aluno.data_nascimento)}</td>
            <td>${aluno.email ? escapeHtml(aluno.email) : '-'}</td>
            <td>${aluno.status}</td>
            <td>${getTurmaNome(aluno.turma_id)}</td>
            <td>
                <button onclick="editAluno(${aluno.id})" 
                        aria-label="Editar aluno ${aluno.nome}">
                    Editar
                </button>
                <button onclick="deleteAluno(${aluno.id})"
                        aria-label="Deletar aluno ${aluno.nome}">
                    Deletar
                </button>
                ${!aluno.turma_id ? `
                    <button onclick="showMatriculaDialog(${aluno.id})"
                            aria-label="Matricular aluno ${aluno.nome}">
                        Matricular
                    </button>
                ` : ''}
            </td>
        </tr>
    `).join('');
}

function updateTurmasSelect() {
    const turmaSelects = document.querySelectorAll('#filtroTurma, #turma');
    const options = ['<option value="">Todas as turmas</option>'];
    
    turmasList.forEach(turma => {
        options.push(`<option value="${turma.id}">${escapeHtml(turma.nome)}</option>`);
    });
    
    turmaSelects.forEach(select => {
        select.innerHTML = options.join('');
    });
}

// Funções de filtragem
function filterAlunos() {
    const turmaId = document.getElementById('filtroTurma').value;
    const status = document.getElementById('filtroStatus').value;
    const busca = document.getElementById('busca').value.toLowerCase();
    
    const filteredAlunos = alunosList.filter(aluno => {
        const matchTurma = !turmaId || aluno.turma_id === parseInt(turmaId);
        const matchStatus = !status || aluno.status === status;
        const matchBusca = !busca || aluno.nome.toLowerCase().includes(busca);
        
        return matchTurma && matchStatus && matchBusca;
    });
    
    updateAlunosTable(filteredAlunos);
}

// Funções de manipulação de alunos
async function handleAlunoSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(alunoForm);
    const dataNascimento = new Date(formData.get('dataNascimento'));
    const alunoData = {
        nome: formData.get('nome'),
        data_nascimento: dataNascimento.toISOString().split('T')[0],
        email: formData.get('email') || null,
        status: formData.get('status'),
        turma_id: formData.get('turma') ? parseInt(formData.get('turma')) : null
    };
    
    try {
        const method = alunoForm.dataset.id ? 'PUT' : 'POST';
        const url = `${API_URL}/alunos${alunoForm.dataset.id ? `/${alunoForm.dataset.id}` : ''}`;
        
        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(alunoData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao salvar aluno');
        }
        
        await loadAlunos();
        alunoModal.close();
        showSuccess('Aluno salvo com sucesso');
    } catch (error) {
        showError(error.message);
        console.error(error);
    }
}

function openAlunoModal(aluno = null) {
    const title = document.getElementById('modalTitle');
    title.textContent = aluno ? 'Editar Aluno' : 'Novo Aluno';
    
    if (aluno) {
        alunoForm.dataset.id = aluno.id;
        document.getElementById('nome').value = aluno.nome;
        // Formata a data no formato YYYY-MM-DD para o input date
        const date = new Date(aluno.data_nascimento);
        date.setDate(date.getDate() + 1);
        document.getElementById('dataNascimento').value = date.toISOString().split('T')[0];
        document.getElementById('email').value = aluno.email || '';
        document.getElementById('status').value = aluno.status;
        document.getElementById('turma').value = aluno.turma_id || '';
    } else {
        alunoForm.dataset.id = '';
        alunoForm.reset();
    }
    
    alunoModal.showModal();
}

async function editAluno(id) {
    try {
        const aluno = alunosList.find(a => a.id === id);
        if (!aluno) {
            throw new Error('Aluno não encontrado');
        }
        openAlunoModal(aluno);
    } catch (error) {
        showError(error.message);
        console.error(error);
    }
}

async function deleteAluno(id) {
    if (!confirm('Tem certeza que deseja deletar este aluno?')) return;
    
    try {
        const response = await fetch(`${API_URL}/alunos/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Erro ao deletar aluno');
        
        await loadAlunos();
        showSuccess('Aluno deletado com sucesso');
    } catch (error) {
        showError('Erro ao deletar aluno');
        console.error(error);
    }
}

// Funções de manipulação de turmas
async function handleTurmaSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(turmaForm);
    const turmaData = {
        nome: formData.get('nomeTurma'),
        capacidade: parseInt(formData.get('capacidade'))
    };
    
    try {
        const response = await fetch(`${API_URL}/turmas`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(turmaData)
        });
        
        if (!response.ok) throw new Error('Erro ao salvar turma');
        
        await loadTurmas();
        turmaModal.close();
        showSuccess('Turma salva com sucesso');
    } catch (error) {
        showError('Erro ao salvar turma');
        console.error(error);
    }
}

function openTurmaModal() {
    turmaForm.reset();
    turmaModal.showModal();
}

// Funções de matrícula
async function showMatriculaDialog(alunoId) {
    const turma = prompt('Digite o ID da turma para matricular o aluno:');
    if (!turma) return;
    
    try {
        const response = await fetch(`${API_URL}/matriculas`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                aluno_id: alunoId, 
                turma_id: parseInt(turma) 
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao matricular aluno');
        }
        
        await Promise.all([loadAlunos(), loadTurmas()]);
        showSuccess('Aluno matriculado com sucesso');
    } catch (error) {
        showError(error.message);
        console.error(error);
    }
}

// Funções de exportação
function exportarAlunos(format) {
    const dados = alunosList.map(aluno => ({
        nome: aluno.nome,
        data_nascimento: aluno.data_nascimento,
        email: aluno.email || '',
        status: aluno.status,
        turma: getTurmaNome(aluno.turma_id)
    }));
    
    if (format === 'csv') {
        const headers = ['Nome', 'Data de Nascimento', 'Email', 'Status', 'Turma'];
        const csv = [
            headers.join(','),
            ...dados.map(row => Object.values(row).join(','))
        ].join('\n');
        
        downloadFile('alunos.csv', csv);
    } else {
        downloadFile('alunos.json', JSON.stringify(dados, null, 2));
    }
}

// Funções de estatísticas
function updateStats() {
    const stats = {
        total: alunosList.length,
        ativos: alunosList.filter(a => a.status === 'ativo').length,
        inativos: alunosList.filter(a => a.status === 'inativo').length,
        porTurma: {}
    };
    
    turmasList.forEach(turma => {
        stats.porTurma[turma.nome] = alunosList.filter(a => a.turma_id === turma.id).length;
    });
    
    const statsContainer = document.getElementById('statsContainer');
    statsContainer.innerHTML = `
        <div class="stat-item">
            <h3>Total de Alunos</h3>
            <p>${stats.total}</p>
        </div>
        <div class="stat-item">
            <h3>Alunos Ativos</h3>
            <p>${stats.ativos}</p>
        </div>
        <div class="stat-item">
            <h3>Alunos Inativos</h3>
            <p>${stats.inativos}</p>
        </div>
        <div class="stat-item">
            <h3>Alunos por Turma</h3>
            ${Object.entries(stats.porTurma).map(([turma, quantidade]) => 
                `<p>${escapeHtml(turma)}: ${quantidade}</p>`
            ).join('')}
        </div>
    `;
}

// Funções auxiliares
function getTurmaNome(turmaId) {
    if (!turmaId) return '-';
    const turma = turmasList.find(t => t.id === turmaId);
    return turma ? escapeHtml(turma.nome) : '-';
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    // Adiciona 1 dia para corrigir o timezone
    date.setDate(date.getDate() + 1);
    return date.toLocaleDateString('pt-BR');
}

function downloadFile(filename, content) {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

function showSuccess(message) {
    alert(message); // Pode ser melhorado com uma notificação mais elegante
}

function showError(message) {
    alert(`Erro: ${message}`); // Pode ser melhorado com uma notificação mais elegante
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}
