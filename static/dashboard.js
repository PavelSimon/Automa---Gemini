let currentUser = null;
let authToken = null;

// Settings
let settings = {
    refreshInterval: 30,
    maxLogEntries: 100,
    autoRefresh: true,
    darkTheme: false
};

// Load settings from localStorage
function loadSettings() {
    const saved = localStorage.getItem('dashboardSettings');
    if (saved) {
        settings = { ...settings, ...JSON.parse(saved) };
    }
    applySettings();
}

function saveSettingsToStorage() {
    localStorage.setItem('dashboardSettings', JSON.stringify(settings));
}

function applySettings() {
    document.getElementById('refreshInterval').value = settings.refreshInterval;
    document.getElementById('maxLogEntries').value = settings.maxLogEntries;
    document.getElementById('autoRefresh').checked = settings.autoRefresh;
    document.getElementById('darkTheme').checked = settings.darkTheme;

    // Apply theme
    applyTheme();
}

function applyTheme() {
    const body = document.body;
    if (settings.darkTheme) {
        body.classList.add('dark-theme');
    } else {
        body.classList.remove('dark-theme');
    }
}

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadSettings();

    // Check if user is logged in
    const token = localStorage.getItem('authToken');
    if (token) {
        authToken = token;
        showMainApp();
    } else {
        showLoginScreen();
    }
});

function showLoginScreen() {
    document.getElementById('login-screen').classList.remove('d-none');
    document.getElementById('main-app').classList.add('d-none');
}

function showMainApp() {
    document.getElementById('login-screen').classList.add('d-none');
    document.getElementById('main-app').classList.remove('d-none');
    showSection('dashboard');
    startAutoRefresh();
}

function showDashboard() {
    refreshData();
}

// Message display function
function showMessage(message, type = 'info') {
    const messageDiv = document.getElementById('authMessage');
    messageDiv.className = `alert alert-${type}`;
    messageDiv.textContent = message;
    messageDiv.classList.remove('d-none');

    // Auto-hide after 5 seconds
    setTimeout(() => {
        messageDiv.classList.add('d-none');
    }, 5000);
}

// Login functions
async function loginWithCredentials() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    if (!email || !password) {
        showMessage('Please enter both email and password', 'warning');
        return;
    }

    // Show loading state
    const btn = document.getElementById('loginBtn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Logging in...';
    btn.disabled = true;

    try {
        const response = await fetch('/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                username: email,
                password: password
            })
        });

        if (response.ok) {
            const data = await response.json();
            authToken = data.access_token;
            localStorage.setItem('authToken', authToken);
            showMessage('Login successful! Welcome to Automa-Gemini.', 'success');
            setTimeout(() => showMainApp(), 1000);
        } else {
            const errorData = await response.json().catch(() => ({}));
            showMessage(errorData.detail || 'Login failed. Please check your credentials.', 'danger');
        }
    } catch (error) {
        console.error('Login error:', error);
        showMessage('Login failed. Please check your connection and try again.', 'danger');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// Registration function
async function registerUser() {
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (!email || !password) {
        showMessage('Please fill in all required fields', 'warning');
        return;
    }

    if (password.length < 6) {
        showMessage('Password must be at least 6 characters long', 'warning');
        return;
    }

    if (password !== confirmPassword) {
        showMessage('Passwords do not match', 'warning');
        return;
    }

    // Show loading state
    const btn = document.getElementById('registerBtn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Creating account...';
    btn.disabled = true;

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        if (response.ok) {
            showMessage('Account created successfully! You can now log in.', 'success');

            // Switch to login tab
            const loginTab = document.getElementById('login-tab');
            const tab = new bootstrap.Tab(loginTab);
            tab.show();

            // Pre-fill login form
            document.getElementById('loginEmail').value = email;

            // Clear registration form
            document.getElementById('registerEmail').value = '';
            document.getElementById('registerPassword').value = '';
            document.getElementById('confirmPassword').value = '';

        } else {
            const errorData = await response.json().catch(() => ({}));
            showMessage(errorData.detail || 'Registration failed. Please try again.', 'danger');
        }
    } catch (error) {
        console.error('Registration error:', error);
        showMessage('Registration failed. Please check your connection and try again.', 'danger');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

function loginWithToken() {
    const token = document.getElementById('apiToken').value.trim();
    if (!token) {
        alert('Please enter a token');
        return;
    }

    // Validate token format (should start with Bearer or just be the token)
    const cleanToken = token.replace('Bearer ', '');
    authToken = cleanToken;
    localStorage.setItem('authToken', cleanToken);
    showMainApp();
}

function logout() {
    authToken = null;
    localStorage.removeItem('authToken');
    stopAutoRefresh();
    showLoginScreen();
}

// Profile functions
async function showProfile() {
    try {
        const response = await fetch('/users/me/', { headers: getAuthHeaders() });
        if (response.ok) {
            const user = await response.json();
            alert(`User Profile:\n\nEmail: ${user.email}\nID: ${user.id}`);
        } else {
            alert('Failed to load user profile');
        }
    } catch (error) {
        console.error('Error loading profile:', error);
        alert('Error loading profile');
    }
}

// Settings functions
function saveSettings() {
    settings.refreshInterval = parseInt(document.getElementById('refreshInterval').value);
    settings.maxLogEntries = parseInt(document.getElementById('maxLogEntries').value);
    settings.autoRefresh = document.getElementById('autoRefresh').checked;
    settings.darkTheme = document.getElementById('darkTheme').checked;

    saveSettingsToStorage();
    applySettings();

    if (settings.autoRefresh) {
        startAutoRefresh();
    } else {
        stopAutoRefresh();
    }

    alert('Settings saved successfully!');
}

function resetSettings() {
    if (confirm('Are you sure you want to reset all settings to defaults?')) {
        settings = {
            refreshInterval: 30,
            maxLogEntries: 100,
            autoRefresh: true,
            darkTheme: false
        };
        saveSettingsToStorage();
        applySettings();
        alert('Settings reset to defaults');
    }
}

// Auto refresh functionality
let autoRefreshInterval = null;

function startAutoRefresh() {
    stopAutoRefresh(); // Clear any existing interval
    if (settings.autoRefresh) {
        autoRefreshInterval = setInterval(refreshData, settings.refreshInterval * 1000);
    }
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
    }
}

// Quick actions
async function testConnection() {
    try {
        const response = await fetch('/', { headers: getAuthHeaders() });
        if (response.ok) {
            alert('✅ API connection successful!');
        } else {
            alert('❌ API connection failed');
        }
    } catch (error) {
        alert('❌ API connection failed: ' + error.message);
    }
}

function clearCache() {
    localStorage.removeItem('dashboardSettings');
    loadSettings();
    alert('Local cache cleared');
}

async function exportData() {
    try {
        const [agentsRes, scriptsRes, tasksRes, logsRes] = await Promise.all([
            fetch('/agents/', { headers: getAuthHeaders() }),
            fetch('/scripts/', { headers: getAuthHeaders() }),
            fetch('/tasks/', { headers: getAuthHeaders() }),
            fetch('/audit/', { headers: getAuthHeaders() })
        ]);

        const data = {
            agents: agentsRes.ok ? await agentsRes.json() : [],
            scripts: scriptsRes.ok ? await scriptsRes.json() : [],
            tasks: tasksRes.ok ? await tasksRes.json() : [],
            audit_logs: logsRes.ok ? await logsRes.json() : [],
            exported_at: new Date().toISOString()
        };

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `automa-gemini-export-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } catch (error) {
        alert('Export failed: ' + error.message);
    }
}

function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.add('d-none');
    });

    // Show selected section
    document.getElementById(sectionName + '-section').classList.remove('d-none');

    // Update active nav link
    document.querySelectorAll('.sidebar .nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelector(`[href="#${sectionName}"]`).classList.add('active');

    // Load section data
    switch(sectionName) {
        case 'agents':
            loadAgents();
            break;
        case 'scripts':
            loadScripts();
            break;
        case 'tasks':
            loadTasks();
            break;
        case 'logs':
            loadLogs();
            break;
    }
}

async function refreshData() {
    try {
        const [agentsRes, scriptsRes, tasksRes] = await Promise.all([
            fetch('/agents/', { headers: getAuthHeaders() }),
            fetch('/scripts/', { headers: getAuthHeaders() }),
            fetch('/tasks/', { headers: getAuthHeaders() })
        ]);

        if (agentsRes.ok) {
            const agents = await agentsRes.json();
            document.getElementById('agents-count').textContent = agents.length;
        }

        if (scriptsRes.ok) {
            const scripts = await scriptsRes.json();
            document.getElementById('scripts-count').textContent = scripts.length;
        }

        if (tasksRes.ok) {
            const tasks = await tasksRes.json();
            document.getElementById('tasks-count').textContent = tasks.length;
            const runningTasks = tasks.filter(t => t.status === 'running').length;
            document.getElementById('running-tasks').textContent = runningTasks;

            // Show recent tasks
            displayRecentTasks(tasks.slice(0, 5));
        }
    } catch (error) {
        console.error('Error refreshing data:', error);
    }
}

function displayRecentTasks(tasks) {
    const container = document.getElementById('recent-tasks');
    if (tasks.length === 0) {
        container.innerHTML = '<p class="text-muted mb-0">No tasks found</p>';
        return;
    }

    container.innerHTML = tasks.map(task => `
        <div class="list-group-item">
            <div class="d-flex w-100 justify-content-between">
                <h6 class="mb-1">${task.name}</h6>
                <small class="text-muted">${new Date(task.created_at).toLocaleString()}</small>
            </div>
            <p class="mb-1">${task.description || 'No description'}</p>
            <small class="text-${getStatusColor(task.status)}">
                <i class="fas ${getStatusIcon(task.status)} me-1"></i>${task.status}
            </small>
        </div>
    `).join('');
}

async function loadAgents() {
    try {
        const response = await fetch('/agents/', { headers: getAuthHeaders() });
        if (response.ok) {
            const agents = await response.json();
            displayAgents(agents);
        }
    } catch (error) {
        console.error('Error loading agents:', error);
    }
}

function displayAgents(agents) {
    const container = document.getElementById('agents-list');
    if (agents.length === 0) {
        container.innerHTML = '<div class="col-12"><p class="text-muted">No agents found</p></div>';
        return;
    }

    container.innerHTML = agents.map(agent => `
        <div class="col-md-4 mb-4">
            <div class="card task-card">
                <div class="card-body">
                    <h5 class="card-title">${agent.name}</h5>
                    <p class="card-text">${agent.description || 'No description'}</p>
                    <span class="badge bg-${agent.status === 'active' ? 'success' : 'secondary'}">
                        ${agent.status}
                    </span>
                </div>
            </div>
        </div>
    `).join('');
}

async function loadScripts() {
    try {
        const response = await fetch('/scripts/', { headers: getAuthHeaders() });
        if (response.ok) {
            const scripts = await response.json();
            displayScripts(scripts);
        }
    } catch (error) {
        console.error('Error loading scripts:', error);
    }
}

function displayScripts(scripts) {
    const container = document.getElementById('scripts-list');
    if (scripts.length === 0) {
        container.innerHTML = '<div class="col-12"><p class="text-muted">No scripts found</p></div>';
        return;
    }

    container.innerHTML = scripts.map(script => `
        <div class="col-md-6 mb-4">
            <div class="card task-card">
                <div class="card-body">
                    <h5 class="card-title">${script.name}</h5>
                    <p class="card-text">${script.description || 'No description'}</p>
                    <small class="text-muted">${script.filename}</small>
                    <div class="mt-2">
                        <button class="btn btn-sm btn-outline-primary me-2" onclick="viewScript(${script.id})">
                            <i class="fas fa-eye"></i> View
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteScript(${script.id})">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

async function loadTasks() {
    try {
        const response = await fetch('/tasks/', { headers: getAuthHeaders() });
        if (response.ok) {
            const tasks = await response.json();
            displayTasks(tasks);
        }
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

function displayTasks(tasks) {
    const container = document.getElementById('tasks-list');
    if (tasks.length === 0) {
        container.innerHTML = '<div class="col-12"><p class="text-muted">No tasks found</p></div>';
        return;
    }

    container.innerHTML = tasks.map(task => `
        <div class="col-md-6 mb-4">
            <div class="card task-card">
                <div class="card-body">
                    <h5 class="card-title">${task.name}</h5>
                    <p class="card-text">${task.description || 'No description'}</p>
                    <div class="mb-2">
                        <span class="badge bg-${getStatusColor(task.status)} me-2">
                            <i class="fas ${getStatusIcon(task.status)} me-1"></i>${task.status}
                        </span>
                        ${task.scheduled_time ? `<small class="text-muted">Scheduled: ${new Date(task.scheduled_time).toLocaleString()}</small>` : ''}
                    </div>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="executeTask(${task.id})">
                            <i class="fas fa-play"></i> Run
                        </button>
                        <button class="btn btn-outline-danger" onclick="deleteTask(${task.id})">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

async function loadLogs() {
    try {
        const response = await fetch('/audit/', { headers: getAuthHeaders() });
        if (response.ok) {
            const logs = await response.json();
            displayLogs(logs);
        }
    } catch (error) {
        console.error('Error loading logs:', error);
    }
}

function displayLogs(logs) {
    const container = document.getElementById('logs-table');
    if (logs.length === 0) {
        container.innerHTML = '<p class="text-muted">No audit logs found</p>';
        return;
    }

    const tableHtml = `
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Time</th>
                    <th>User</th>
                    <th>Action</th>
                    <th>Resource</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
                ${logs.map(log => `
                    <tr>
                        <td>${new Date(log.timestamp).toLocaleString()}</td>
                        <td>${log.user_id || 'System'}</td>
                        <td>${log.action}</td>
                        <td>${log.resource_type} ${log.resource_id || ''}</td>
                        <td><small>${log.details || ''}</small></td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    container.innerHTML = tableHtml;
}

function getAuthHeaders() {
    return authToken ? { 'Authorization': `Bearer ${authToken}` } : {};
}

function getStatusColor(status) {
    switch(status) {
        case 'completed': return 'success';
        case 'running': return 'primary';
        case 'failed': return 'danger';
        case 'pending': return 'warning';
        default: return 'secondary';
    }
}

function getStatusIcon(status) {
    switch(status) {
        case 'completed': return 'fa-check-circle';
        case 'running': return 'fa-play-circle';
        case 'failed': return 'fa-times-circle';
        case 'pending': return 'fa-clock';
        default: return 'fa-question-circle';
    }
}

// Placeholder functions for form handling
async function saveAgent() {
    const formData = {
        name: document.getElementById('agentName').value,
        description: document.getElementById('agentDescription').value,
        status: document.getElementById('agentStatus').value
    };

    try {
        const response = await fetch('/agents/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...getAuthHeaders()
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('agentModal')).hide();
            loadAgents();
            refreshData();
        } else {
            alert('Error saving agent');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error saving agent');
    }
}

async function saveScript() {
    const formData = {
        name: document.getElementById('scriptName').value,
        description: document.getElementById('scriptDescription').value,
        filename: document.getElementById('scriptFilename').value || 'script.py',
        content: document.getElementById('scriptContent').value
    };

    try {
        const response = await fetch('/scripts/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...getAuthHeaders()
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('scriptModal')).hide();
            loadScripts();
            refreshData();
        } else {
            alert('Error saving script');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error saving script');
    }
}

async function saveTask() {
    const scheduledTime = document.getElementById('taskScheduledTime').value;
    const formData = {
        name: document.getElementById('taskName').value,
        description: document.getElementById('taskDescription').value,
        agent_id: parseInt(document.getElementById('taskAgent').value),
        script_id: parseInt(document.getElementById('taskScript').value),
        scheduled_time: scheduledTime ? new Date(scheduledTime).toISOString() : null
    };

    try {
        const response = await fetch('/tasks/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...getAuthHeaders()
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('taskModal')).hide();
            loadTasks();
            refreshData();
        } else {
            alert('Error creating task');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error creating task');
    }
}

async function executeTask(taskId) {
    try {
        const response = await fetch(`/tasks/${taskId}/execute`, {
            method: 'POST',
            headers: getAuthHeaders()
        });

        if (response.ok) {
            alert('Task execution started');
            refreshData();
        } else {
            alert('Error executing task');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error executing task');
    }
}

function refreshLogs() {
    loadLogs();
}

// Load agents and scripts for task creation
document.getElementById('taskModal').addEventListener('show.bs.modal', async function() {
    try {
        const [agentsRes, scriptsRes] = await Promise.all([
            fetch('/agents/', { headers: getAuthHeaders() }),
            fetch('/scripts/', { headers: getAuthHeaders() })
        ]);

        if (agentsRes.ok) {
            const agents = await agentsRes.json();
            const agentSelect = document.getElementById('taskAgent');
            agentSelect.innerHTML = '<option value="">Select Agent</option>' +
                agents.map(agent => `<option value="${agent.id}">${agent.name}</option>`).join('');
        }

        if (scriptsRes.ok) {
            const scripts = await scriptsRes.json();
            const scriptSelect = document.getElementById('taskScript');
            scriptSelect.innerHTML = '<option value="">Select Script</option>' +
                scripts.map(script => `<option value="${script.id}">${script.name}</option>`).join('');
        }
    } catch (error) {
        console.error('Error loading agents/scripts:', error);
    }
});
