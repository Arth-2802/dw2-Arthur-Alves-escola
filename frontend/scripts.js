/**
 * SISTEMA DE GESTÃO ESCOLAR - JAVASCRIPT
 * 
 * Este arquivo contém toda a lógica frontend do sistema:
 * - Comunicação com API REST
 * - Manipulação do DOM
 * - Validações de formulário
 * - Filtros e busca em tempo real
 * - Acessibilidade e navegação por teclado
 * - Gerenciamento de estado da aplicação
 */

// ===== CONFIGURAÇÃO DA API =====
const API_BASE_URL = 'http://localhost:8001';

// ===== ESTADO DA APLICAÇÃO =====
let appState = {
    alunos: [],
    turmas: [],
    filtros: {
        search: '',
        turma_id: '',
        status: ''
    },
    ordenacao: 'nome',
    tabAtiva: 'alunos',
    usuario: null,
    token: localStorage.getItem('auth_token') || null
};

// ===== UTILITÁRIOS =====

/**
 * Faz requisição HTTP para a API
 * @param {string} url - URL do endpoint
 * @param {Object} options - Opções da requisição
 * @returns {Promise} - Resposta da API
 */
async function apiRequest(url, options = {}) {
    try {
        console.log(`🔗 API Request: ${url}`, options); // Debug log
        
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        
        // Adiciona token de autenticação se disponível (exceto para endpoints de auth)
        if (appState.token && !url.startsWith('/auth/')) {
            headers['Authorization'] = `Bearer ${appState.token}`;
        }
        
        const response = await fetch(`${API_BASE_URL}${url}`, {
            headers,
            ...options
        });

        console.log(`📡 Response Status: ${response.status}`, response); // Debug log

        // Se token expirou, redireciona para login
        if (response.status === 401 && appState.token) {
            console.log('🔐 Token expirado, fazendo logout');
            logout();
            return;
        }

        const data = await response.json();
        console.log(`📄 Response Data:`, data); // Debug log

        if (!response.ok) {
            throw new Error(data.detail || `Erro ${response.status}`);
        }

        return data;
    } catch (error) {
        console.error('❌ Erro na API:', error);
        throw error;
    }
}

/**
 * Exibe notificação toast
 * @param {string} message - Mensagem a ser exibida
 * @param {string} type - Tipo: success, error, warning, info
 * @param {number} duration - Duração em ms (default: 5000)
 */
function showToast(message, type = 'info', duration = 5000) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    };

    const titles = {
        success: 'Sucesso',
        error: 'Erro',
        warning: 'Atenção',
        info: 'Informação'
    };

    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="toast-icon ${icons[type]}" aria-hidden="true"></i>
        <div class="toast-content">
            <div class="toast-title">${titles[type]}</div>
            <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close" aria-label="Fechar notificação">
            <i class="fas fa-times" aria-hidden="true"></i>
        </button>
    `;

    // Adicionar evento de fechar
    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', () => {
        toast.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    });

    container.appendChild(toast);

    // Auto-remover após duração especificada
    setTimeout(() => {
        if (toast.parentNode) {
            toast.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }
    }, duration);
}

// ===== FUNÇÕES DE AUTENTICAÇÃO =====

/**
 * Realiza login do usuário
 * @param {string} username - Nome de usuário
 * @param {string} senha - Senha do usuário
 * @returns {Promise} - Resposta da API
 */
async function login(username, senha) {
    try {
        const response = await apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({
                username: username,
                senha: senha
            })
        });
        
        if (response.access_token) {
            // Armazena token e dados do usuário
            appState.token = response.access_token;
            appState.usuario = response.usuario;
            localStorage.setItem('auth_token', response.access_token);
            localStorage.setItem('user_data', JSON.stringify(response.usuario));
            
            showToast('Login realizado com sucesso!', 'success');
            mostrarApp();
            return response;
        }
    } catch (error) {
        console.error('Erro no login:', error);
        showToast('Erro no login: ' + error.message, 'error');
        throw error;
    }
}

/**
 * Realiza logout do usuário
 */
function logout() {
    appState.token = null;
    appState.usuario = null;
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_data');
    
    mostrarLogin();
    showToast('Logout realizado com sucesso!', 'info');
}

/**
 * Verifica se o usuário está autenticado
 * @returns {boolean} - True se autenticado
 */
function isAuthenticated() {
    return !!appState.token;
}

/**
 * Obtém dados do usuário do perfil
 */
async function obterPerfil() {
    try {
        if (!isAuthenticated()) {
            throw new Error('Usuário não autenticado');
        }
        
        const usuario = await apiRequest('/auth/me');
        appState.usuario = usuario;
        localStorage.setItem('user_data', JSON.stringify(usuario));
        
        return usuario;
    } catch (error) {
        console.error('Erro ao obter perfil:', error);
        logout();
        throw error;
    }
}

/**
 * Mostra a tela de login
 */
function mostrarLogin() {
    document.getElementById('login-screen').classList.remove('hidden');
    document.getElementById('main-app').classList.add('hidden');
}

/**
 * Mostra a aplicação principal
 */
function mostrarApp() {
    document.getElementById('login-screen').classList.add('hidden');
    document.getElementById('main-app').classList.remove('hidden');
    
    // Atualiza nome do usuário no cabeçalho
    if (appState.usuario) {
        document.getElementById('user-name').textContent = appState.usuario.nome_completo;
    }
    
    // Inicializa dados da aplicação
    inicializarApp();
}

/**
 * Formatar data para exibição
 * @param {string} dateString - Data em formato ISO
 * @returns {string} - Data formatada
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

/**
 * Calcular idade baseada na data de nascimento
 * @param {string} birthDate - Data de nascimento
 * @returns {number} - Idade em anos
 */
function calculateAge(birthDate) {
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
        age--;
    }
    
    return age;
}

/**
 * Sanitizar string para prevenir XSS
 * @param {string} str - String a ser sanitizada
 * @returns {string} - String sanitizada
 */
function sanitizeHTML(str) {
    const temp = document.createElement('div');
    temp.textContent = str;
    return temp.innerHTML;
}

// ===== VALIDAÇÕES =====

/**
 * Validar email
 * @param {string} email - Email a ser validado
 * @returns {boolean} - True se válido
 */
function isValidEmail(email) {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email);
}

/**
 * Validar idade mínima
 * @param {string} birthDate - Data de nascimento
 * @returns {boolean} - True se idade >= 5 anos
 */
function isValidAge(birthDate) {
    return calculateAge(birthDate) >= 5;
}

/**
 * Validar formulário de aluno
 * @param {FormData} formData - Dados do formulário
 * @returns {Object} - {isValid: boolean, errors: {}}
 */
function validateAlunoForm(formData) {
    const errors = {};
    let isValid = true;

    // Nome (obrigatório, 3-80 caracteres)
    const nome = formData.get('nome')?.trim();
    if (!nome) {
        errors.nome = 'Nome é obrigatório';
        isValid = false;
    } else if (nome.length < 3) {
        errors.nome = 'Nome deve ter pelo menos 3 caracteres';
        isValid = false;
    } else if (nome.length > 80) {
        errors.nome = 'Nome deve ter no máximo 80 caracteres';
        isValid = false;
    }

    // Data de nascimento (obrigatória, idade >= 5 anos)
    const dataNascimento = formData.get('data_nascimento');
    if (!dataNascimento) {
        errors.data_nascimento = 'Data de nascimento é obrigatória';
        isValid = false;
    } else if (!isValidAge(dataNascimento)) {
        errors.data_nascimento = 'Aluno deve ter pelo menos 5 anos de idade';
        isValid = false;
    }

    // Email (opcional, mas deve ser válido se fornecido)
    const email = formData.get('email')?.trim();
    if (email && !isValidEmail(email)) {
        errors.email = 'Formato de email inválido';
        isValid = false;
    }

    return { isValid, errors };
}

/**
 * Exibir erros de validação no formulário
 * @param {Object} errors - Objeto com erros por campo
 */
function displayFormErrors(errors) {
    // Limpar erros anteriores
    document.querySelectorAll('.error-message').forEach(el => {
        el.textContent = '';
    });
    document.querySelectorAll('.form-input, .form-select').forEach(el => {
        el.classList.remove('error');
    });

    // Exibir novos erros
    Object.entries(errors).forEach(([field, message]) => {
        const errorElement = document.getElementById(`${field.replace('_', '-')}-error`);
        const inputElement = document.getElementById(`aluno-${field.replace('_', '-')}`);
        
        if (errorElement) {
            errorElement.textContent = message;
        }
        if (inputElement) {
            inputElement.classList.add('error');
        }
    });
}

// ===== GERENCIAMENTO DE MODAIS =====

/**
 * Abrir modal
 * @param {string} modalId - ID do modal
 */
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        
        // Focar no primeiro elemento focável
        const firstFocusable = modal.querySelector('input, select, button, textarea');
        if (firstFocusable) {
            setTimeout(() => firstFocusable.focus(), 100);
        }

        // Gerenciar foco no modal (trap focus)
        modal.addEventListener('keydown', handleModalKeydown);
    }
}

/**
 * Fechar modal
 * @param {string} modalId - ID do modal
 */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
        
        // Limpar formulário se houver
        const form = modal.querySelector('form');
        if (form) {
            form.reset();
            // Limpar erros
            modal.querySelectorAll('.error-message').forEach(el => {
                el.textContent = '';
            });
            modal.querySelectorAll('.form-input, .form-select').forEach(el => {
                el.classList.remove('error');
            });
        }

        modal.removeEventListener('keydown', handleModalKeydown);
    }
}

/**
 * Gerenciar navegação por teclado no modal
 * @param {KeyboardEvent} e - Evento de teclado
 */
function handleModalKeydown(e) {
    if (e.key === 'Escape') {
        const modal = e.currentTarget;
        const modalId = modal.id;
        closeModal(modalId);
        return;
    }

    // Trap focus dentro do modal
    if (e.key === 'Tab') {
        const modal = e.currentTarget;
        const focusableElements = modal.querySelectorAll(
            'input, select, button, textarea, [tabindex]:not([tabindex="-1"])'
        );
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (e.shiftKey) {
            if (document.activeElement === firstElement) {
                lastElement.focus();
                e.preventDefault();
            }
        } else {
            if (document.activeElement === lastElement) {
                firstElement.focus();
                e.preventDefault();
            }
        }
    }
}

// ===== OPERAÇÕES DE DADOS =====

/**
 * Carregar lista de alunos da API
 */
async function loadAlunos() {
    try {
        showLoading('alunos');
        
        const params = new URLSearchParams();
        if (appState.filtros.search) params.append('search', appState.filtros.search);
        if (appState.filtros.turma_id) params.append('turma_id', appState.filtros.turma_id);
        if (appState.filtros.status) params.append('status', appState.filtros.status);

        const queryString = params.toString();
        const url = queryString ? `/alunos?${queryString}` : '/alunos';
        
        appState.alunos = await apiRequest(url);
        
        // Aplicar ordenação
        sortAlunos(appState.ordenacao);
        
        renderAlunos();
        updateStatistics();
        
    } catch (error) {
        showToast(`Erro ao carregar alunos: ${error.message}`, 'error');
        hideLoading('alunos');
    }
}

/**
 * Carregar lista de turmas da API
 */
async function loadTurmas() {
    try {
        showLoading('turmas');
        
        appState.turmas = await apiRequest('/turmas');
        
        renderTurmas();
        updateTurmaSelects();
        updateStatistics();
        
    } catch (error) {
        showToast(`Erro ao carregar turmas: ${error.message}`, 'error');
        hideLoading('turmas');
    }
}

/**
 * Criar novo aluno
 * @param {Object} alunoData - Dados do aluno
 */
async function createAluno(alunoData) {
    try {
        await apiRequest('/alunos', {
            method: 'POST',
            body: JSON.stringify(alunoData)
        });

        showToast('Aluno criado com sucesso!', 'success');
        closeModal('modal-aluno');
        loadAlunos();
        
    } catch (error) {
        showToast(`Erro ao criar aluno: ${error.message}`, 'error');
    }
}

/**
 * Atualizar aluno existente
 * @param {number} id - ID do aluno
 * @param {Object} alunoData - Dados atualizados
 */
async function updateAluno(id, alunoData) {
    try {
        await apiRequest(`/alunos/${id}`, {
            method: 'PUT',
            body: JSON.stringify(alunoData)
        });

        showToast('Aluno atualizado com sucesso!', 'success');
        closeModal('modal-aluno');
        loadAlunos();
        
    } catch (error) {
        showToast(`Erro ao atualizar aluno: ${error.message}`, 'error');
    }
}

/**
 * Excluir aluno
 * @param {number} id - ID do aluno
 */
async function deleteAluno(id) {
    if (!confirm('Tem certeza que deseja excluir este aluno?')) {
        return;
    }

    try {
        await apiRequest(`/alunos/${id}`, {
            method: 'DELETE'
        });

        showToast('Aluno excluído com sucesso!', 'success');
        loadAlunos();
        
    } catch (error) {
        showToast(`Erro ao excluir aluno: ${error.message}`, 'error');
    }
}

/**
 * Criar nova turma
 * @param {Object} turmaData - Dados da turma
 */
async function createTurma(turmaData) {
    try {
        await apiRequest('/turmas', {
            method: 'POST',
            body: JSON.stringify(turmaData)
        });

        showToast('Turma criada com sucesso!', 'success');
        closeModal('modal-turma');
        loadTurmas();
        
    } catch (error) {
        showToast(`Erro ao criar turma: ${error.message}`, 'error');
    }
}

/**
 * Matricular aluno em turma
 * @param {Object} matriculaData - Dados da matrícula
 */
async function matricularAluno(matriculaData) {
    try {
        await apiRequest('/matriculas', {
            method: 'POST',
            body: JSON.stringify(matriculaData)
        });

        showToast('Aluno matriculado com sucesso!', 'success');
        closeModal('modal-matricula');
        
        // Recarregar dados
        loadAlunos();
        loadTurmas();
        
    } catch (error) {
        showToast(`Erro ao matricular aluno: ${error.message}`, 'error');
    }
}

// ===== RENDERIZAÇÃO =====

/**
 * Exibir indicador de carregamento
 * @param {string} section - Seção (alunos ou turmas)
 */
function showLoading(section) {
    const loadingElement = document.getElementById(`loading-${section}`);
    if (loadingElement) {
        loadingElement.style.display = 'flex';
    }
    
    // Ocultar conteúdo
    const contentElement = section === 'alunos' 
        ? document.querySelector('.table-container')
        : document.getElementById('turmas-grid');
    
    if (contentElement) {
        contentElement.style.display = 'none';
    }
}

/**
 * Ocultar indicador de carregamento
 * @param {string} section - Seção (alunos ou turmas)
 */
function hideLoading(section) {
    const loadingElement = document.getElementById(`loading-${section}`);
    if (loadingElement) {
        loadingElement.style.display = 'none';
    }
    
    // Mostrar conteúdo
    const contentElement = section === 'alunos' 
        ? document.querySelector('.table-container')
        : document.getElementById('turmas-grid');
    
    if (contentElement) {
        contentElement.style.display = 'block';
    }
}

/**
 * Renderizar lista de alunos
 */
function renderAlunos() {
    const tbody = document.getElementById('alunos-tbody');
    const noResults = document.getElementById('no-results');
    
    hideLoading('alunos');
    
    if (!appState.alunos || appState.alunos.length === 0) {
        tbody.innerHTML = '';
        noResults.style.display = 'block';
        document.querySelector('.table-container').style.display = 'none';
        return;
    }
    
    noResults.style.display = 'none';
    document.querySelector('.table-container').style.display = 'block';
    
    tbody.innerHTML = appState.alunos.map(aluno => `
        <tr>
            <td>
                <strong>${sanitizeHTML(aluno.nome)}</strong>
            </td>
            <td>${aluno.idade || calculateAge(aluno.data_nascimento)} anos</td>
            <td>${aluno.email ? sanitizeHTML(aluno.email) : '<span style="color: var(--gray-400);">Não informado</span>'}</td>
            <td>
                <span class="status-badge ${aluno.status}">
                    ${aluno.status}
                </span>
            </td>
            <td>${aluno.turma_nome ? sanitizeHTML(aluno.turma_nome) : '<span style="color: var(--gray-400);">Sem turma</span>'}</td>
            <td>
                <div class="actions">
                    <button 
                        class="btn btn-sm btn-secondary" 
                        onclick="editAluno(${aluno.id})"
                        aria-label="Editar aluno ${sanitizeHTML(aluno.nome)}"
                    >
                        <i class="fas fa-edit" aria-hidden="true"></i>
                    </button>
                    <button 
                        class="btn btn-sm btn-danger" 
                        onclick="deleteAluno(${aluno.id})"
                        aria-label="Excluir aluno ${sanitizeHTML(aluno.nome)}"
                    >
                        <i class="fas fa-trash" aria-hidden="true"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

/**
 * Renderizar grid de turmas
 */
function renderTurmas() {
    const grid = document.getElementById('turmas-grid');
    
    hideLoading('turmas');
    
    if (!appState.turmas || appState.turmas.length === 0) {
        grid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: var(--spacing-16); color: var(--gray-500);">
                <i class="fas fa-chalkboard" style="font-size: var(--font-size-3xl); margin-bottom: var(--spacing-4);"></i>
                <p>Nenhuma turma cadastrada ainda.</p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = appState.turmas.map(turma => {
        const ocupacaoPercent = turma.capacidade > 0 ? (turma.ocupacao / turma.capacidade) * 100 : 0;
        let progressClass = '';
        
        if (ocupacaoPercent >= 90) {
            progressClass = 'danger';
        } else if (ocupacaoPercent >= 75) {
            progressClass = 'warning';
        }
        
        return `
            <div class="turma-card">
                <div class="turma-card-header">
                    <h3 class="turma-nome">${sanitizeHTML(turma.nome)}</h3>
                    <span class="turma-ocupacao">
                        ${turma.ocupacao}/${turma.capacidade}
                    </span>
                </div>
                
                <div class="turma-info">
                    <div class="info-item">
                        <div class="info-value">${turma.capacidade}</div>
                        <div class="info-label">Capacidade</div>
                    </div>
                    <div class="info-item">
                        <div class="info-value">${turma.ocupacao}</div>
                        <div class="info-label">Matriculados</div>
                    </div>
                </div>
                
                <div class="progress-bar">
                    <div 
                        class="progress-fill ${progressClass}" 
                        style="width: ${ocupacaoPercent}%"
                        role="progressbar"
                        aria-valuenow="${turma.ocupacao}"
                        aria-valuemin="0"
                        aria-valuemax="${turma.capacidade}"
                        aria-label="Ocupação da turma: ${turma.ocupacao} de ${turma.capacidade} alunos"
                    ></div>
                </div>
                
                <div style="text-align: center; margin-top: var(--spacing-4); font-size: var(--font-size-sm); color: var(--gray-600);">
                    ${ocupacaoPercent.toFixed(1)}% ocupada
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Atualizar estatísticas exibidas na sidebar
 */
function updateStatistics() {
    const totalAlunosEl = document.getElementById('total-alunos');
    const alunosAtivosEl = document.getElementById('alunos-ativos');
    const totalTurmasEl = document.getElementById('total-turmas');
    
    if (totalAlunosEl) {
        totalAlunosEl.textContent = appState.alunos ? appState.alunos.length : 0;
    }
    
    if (alunosAtivosEl) {
        const ativos = appState.alunos ? appState.alunos.filter(a => a.status === 'ativo').length : 0;
        alunosAtivosEl.textContent = ativos;
    }
    
    if (totalTurmasEl) {
        totalTurmasEl.textContent = appState.turmas ? appState.turmas.length : 0;
    }
}

/**
 * Atualizar selects de turma nos formulários
 */
function updateTurmaSelects() {
    const selects = [
        document.getElementById('filter-turma'),
        document.getElementById('aluno-turma'),
        document.getElementById('matricula-turma')
    ];
    
    selects.forEach(select => {
        if (!select) return;
        
        // Manter opção padrão
        const defaultOption = select.querySelector('option[value=""]');
        select.innerHTML = '';
        if (defaultOption) {
            select.appendChild(defaultOption);
        }
        
        // Adicionar turmas
        appState.turmas.forEach(turma => {
            const option = document.createElement('option');
            option.value = turma.id;
            option.textContent = turma.nome;
            select.appendChild(option);
        });
    });
}

/**
 * Atualizar select de alunos para matrícula
 */
function updateAlunosSelect() {
    const select = document.getElementById('matricula-aluno');
    if (!select) return;
    
    // Manter opção padrão
    select.innerHTML = '<option value="">Selecione um aluno</option>';
    
    // Adicionar apenas alunos inativos ou sem turma
    const alunosDisponiveis = appState.alunos.filter(aluno => 
        aluno.status === 'inativo' || !aluno.turma_id
    );
    
    alunosDisponiveis.forEach(aluno => {
        const option = document.createElement('option');
        option.value = aluno.id;
        option.textContent = `${aluno.nome} (${aluno.idade || calculateAge(aluno.data_nascimento)} anos)`;
        select.appendChild(option);
    });
}

// ===== FILTROS E ORDENAÇÃO =====

/**
 * Aplicar filtros aos alunos
 */
function applyFilters() {
    loadAlunos(); // Recarregar com novos filtros
}

/**
 * Limpar todos os filtros
 */
function clearFilters() {
    appState.filtros = {
        search: '',
        turma_id: '',
        status: ''
    };
    
    // Limpar campos de filtro
    document.getElementById('search-input').value = '';
    document.getElementById('filter-turma').value = '';
    document.getElementById('filter-status').value = '';
    
    // Recarregar alunos
    loadAlunos();
}

/**
 * Ordenar array de alunos
 * @param {string} criteria - Critério de ordenação
 */
function sortAlunos(criteria) {
    if (!appState.alunos) return;
    
    appState.alunos.sort((a, b) => {
        switch (criteria) {
            case 'nome':
                return a.nome.localeCompare(b.nome);
            case 'nome-desc':
                return b.nome.localeCompare(a.nome);
            case 'idade':
                const idadeA = a.idade || calculateAge(a.data_nascimento);
                const idadeB = b.idade || calculateAge(b.data_nascimento);
                return idadeA - idadeB;
            case 'idade-desc':
                const idadeA2 = a.idade || calculateAge(a.data_nascimento);
                const idadeB2 = b.idade || calculateAge(b.data_nascimento);
                return idadeB2 - idadeA2;
            default:
                return 0;
        }
    });
}

// ===== OPERAÇÕES DE EDIÇÃO =====

/**
 * Abrir modal para editar aluno
 * @param {number} id - ID do aluno
 */
function editAluno(id) {
    const aluno = appState.alunos.find(a => a.id === id);
    if (!aluno) {
        showToast('Aluno não encontrado', 'error');
        return;
    }
    
    // Preencher formulário
    document.getElementById('aluno-nome').value = aluno.nome;
    document.getElementById('aluno-nascimento').value = aluno.data_nascimento;
    document.getElementById('aluno-email').value = aluno.email || '';
    document.getElementById('aluno-status').value = aluno.status;
    document.getElementById('aluno-turma').value = aluno.turma_id || '';
    
    // Alterar título do modal
    document.getElementById('modal-aluno-title').textContent = 'Editar Aluno';
    
    // Marcar formulário como edição
    const form = document.getElementById('form-aluno');
    form.dataset.mode = 'edit';
    form.dataset.id = id;
    
    openModal('modal-aluno');
}

// ===== GERENCIAMENTO DE TABS =====

/**
 * Alternar entre tabs
 * @param {string} tabName - Nome da tab
 */
function switchTab(tabName) {
    // Atualizar estado
    appState.tabAtiva = tabName;
    
    // Atualizar botões de tab
    document.querySelectorAll('.tab-btn').forEach(btn => {
        const isActive = btn.dataset.tab === tabName;
        btn.classList.toggle('active', isActive);
        btn.setAttribute('aria-pressed', isActive);
    });
    
    // Atualizar conteúdo das tabs
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.toggle('active', content.id === `tab-${tabName}`);
    });
    
    // Carregar dados se necessário
    if (tabName === 'alunos' && !appState.alunos.length) {
        loadAlunos();
    } else if (tabName === 'turmas' && !appState.turmas.length) {
        loadTurmas();
    }
}

// ===== EVENT LISTENERS =====

/**
 * Inicializa event listeners do login
 */
function initLoginListeners() {
    // Form de login
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;
            
            if (!username || !password) {
                showToast('Preencha todos os campos', 'warning');
                return;
            }
            
            // Mostra loading
            const form = document.getElementById('login-form');
            const loading = document.getElementById('login-loading');
            form.classList.add('hidden');
            loading.classList.remove('hidden');
            
            try {
                await login(username, password);
            } catch (error) {
                // Volta para o form em caso de erro
                form.classList.remove('hidden');
                loading.classList.add('hidden');
            }
        });
    }
    
    // Botão para mostrar/esconder senha
    const togglePassword = document.querySelector('.toggle-password');
    if (togglePassword) {
        togglePassword.addEventListener('click', () => {
            const passwordInput = document.getElementById('password');
            const icon = togglePassword.querySelector('i');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.classList.replace('fa-eye', 'fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                icon.classList.replace('fa-eye-slash', 'fa-eye');
            }
        });
    }
}

/**
 * Inicializar todos os event listeners da aplicação principal
 */
function initEventListeners() {
    // === NAVEGAÇÃO POR TABS ===
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            switchTab(btn.dataset.tab);
        });
    });
    
    // === BUSCA ===
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.querySelector('.search-btn');
    
    let searchTimeout;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            appState.filtros.search = e.target.value.trim();
            applyFilters();
        }, 300); // Debounce de 300ms
    });
    
    searchBtn.addEventListener('click', () => {
        appState.filtros.search = searchInput.value.trim();
        applyFilters();
    });
    
    // Busca ao pressionar Enter
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            appState.filtros.search = e.target.value.trim();
            applyFilters();
        }
    });
    
    // === FILTROS ===
    document.getElementById('filter-turma').addEventListener('change', (e) => {
        appState.filtros.turma_id = e.target.value;
        applyFilters();
    });
    
    document.getElementById('filter-status').addEventListener('change', (e) => {
        appState.filtros.status = e.target.value;
        applyFilters();
    });
    
    document.getElementById('clear-filters').addEventListener('click', clearFilters);
    
    // === ORDENAÇÃO ===
    document.getElementById('sort-select').addEventListener('change', (e) => {
        appState.ordenacao = e.target.value;
        sortAlunos(appState.ordenacao);
        renderAlunos();
    });
    
    // === BOTÕES DE AÇÃO ===
    document.getElementById('btn-novo-aluno').addEventListener('click', () => {
        // Resetar formulário para modo criação
        const form = document.getElementById('form-aluno');
        form.dataset.mode = 'create';
        delete form.dataset.id;
        document.getElementById('modal-aluno-title').textContent = 'Novo Aluno';
        
        openModal('modal-aluno');
    });
    
    document.getElementById('btn-nova-turma').addEventListener('click', () => {
        openModal('modal-turma');
    });
    
    document.getElementById('btn-matricula').addEventListener('click', () => {
        updateAlunosSelect(); // Atualizar lista de alunos disponíveis
        openModal('modal-matricula');
    });
    
    // === MODAIS - FECHAR ===
    document.querySelectorAll('.modal-close, .modal-overlay').forEach(element => {
        element.addEventListener('click', (e) => {
            const modal = e.target.closest('.modal');
            if (modal && (e.target.classList.contains('modal-close') || e.target.classList.contains('modal-overlay'))) {
                closeModal(modal.id);
            }
        });
    });
    
    document.querySelectorAll('[id^="btn-cancelar-"]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const modal = e.target.closest('.modal');
            if (modal) {
                closeModal(modal.id);
            }
        });
    });
    
    // === FORMULÁRIOS ===
    
    // Formulário de Aluno
    document.getElementById('form-aluno').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const form = e.target;
        const formData = new FormData(form);
        
        // Validar formulário
        const validation = validateAlunoForm(formData);
        if (!validation.isValid) {
            displayFormErrors(validation.errors);
            return;
        }
        
        // Preparar dados
        const alunoData = {
            nome: formData.get('nome').trim(),
            data_nascimento: formData.get('data_nascimento'),
            email: formData.get('email')?.trim() || null,
            status: formData.get('status'),
            turma_id: formData.get('turma_id') ? parseInt(formData.get('turma_id')) : null
        };
        
        // Criar ou atualizar
        if (form.dataset.mode === 'edit') {
            await updateAluno(parseInt(form.dataset.id), alunoData);
        } else {
            await createAluno(alunoData);
        }
    });
    
    // Formulário de Turma
    document.getElementById('form-turma').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const turmaData = {
            nome: formData.get('nome').trim(),
            capacidade: parseInt(formData.get('capacidade'))
        };
        
        await createTurma(turmaData);
    });
    
    // Formulário de Matrícula
    document.getElementById('form-matricula').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const matriculaData = {
            aluno_id: parseInt(formData.get('aluno_id')),
            turma_id: parseInt(formData.get('turma_id'))
        };
        
        await matricularAluno(matriculaData);
    });
    
    // === VALIDAÇÃO EM TEMPO REAL ===
    
    // Validação de email
    document.getElementById('aluno-email').addEventListener('blur', (e) => {
        const email = e.target.value.trim();
        const errorEl = document.getElementById('email-error');
        
        if (email && !isValidEmail(email)) {
            errorEl.textContent = 'Formato de email inválido';
            e.target.classList.add('error');
        } else {
            errorEl.textContent = '';
            e.target.classList.remove('error');
        }
    });
    
    // Validação de idade
    document.getElementById('aluno-nascimento').addEventListener('blur', (e) => {
        const date = e.target.value;
        const errorEl = document.getElementById('nascimento-error');
        
        if (date && !isValidAge(date)) {
            errorEl.textContent = 'Aluno deve ter pelo menos 5 anos de idade';
            e.target.classList.add('error');
        } else {
            errorEl.textContent = '';
            e.target.classList.remove('error');
        }
    });
    
    // === ACESSIBILIDADE - NAVEGAÇÃO POR TECLADO ===
    
    // Escape para fechar modais
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal[style*="flex"]');
            if (openModal) {
                closeModal(openModal.id);
            }
        }
    });
    
    // Enter em elementos focáveis
    document.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && e.target.matches('th[tabindex="0"]')) {
            e.target.click();
        }
    });
    
    // === LOGOUT ===
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            logout();
        });
    }
}

// ===== INICIALIZAÇÃO =====

/**
 * Inicializar aplicação
 */
async function initApp() {
    try {
        console.log('🚀 Inicializando Sistema de Gestão Escolar...');
        
        // Verifica se há token armazenado
        if (appState.token) {
            try {
                // Tenta obter dados do usuário
                await obterPerfil();
                mostrarApp();
                return;
            } catch (error) {
                // Token inválido, remove e mostra login
                console.log('Token inválido, redirecionando para login');
                logout();
            }
        }
        
        // Se não há token ou token inválido, mostra login
        mostrarLogin();
        initLoginListeners();
        
    } catch (error) {
        console.error('❌ Erro ao inicializar sistema:', error);
        mostrarLogin();
        initLoginListeners();
    }
}

/**
 * Inicializa a aplicação principal (após login)
 */
async function inicializarApp() {
    try {
        console.log('🔄 Carregando dados da aplicação...');
        
        // Configurar event listeners da app principal
        initEventListeners();
        
        // Carregar dados iniciais
        await Promise.all([
            loadAlunos(),
            loadTurmas()
        ]);
        
        console.log('✅ Aplicação carregada com sucesso!');
        
    } catch (error) {
        console.error('❌ Erro ao carregar aplicação:', error);
        showToast('Erro ao carregar dados. Tente novamente.', 'error');
    }
}

// ===== EXECUÇÃO =====

// Aguardar DOM estar pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}

// ===== FUNÇÕES GLOBAIS (para uso em onclick nos templates) =====

// Tornar funções acessíveis globalmente
window.editAluno = editAluno;
window.deleteAluno = deleteAluno;
