/**
 * WareSoft DevNexus API & Interface Handlers
 * Centralized fetch client, error boundaries, toast notifications and sidebar state
 */

const WareSoftAPI = (function() {
    // ─── Toast System ───
    function showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toastId = 'toast-' + Date.now();
        const iconMap = {
            success: 'bi-check-circle-fill ws-text-cyan',
            warning: 'bi-exclamation-triangle-fill ws-text-blue',
            danger: 'bi-x-circle-fill ws-text-ink',
            info: 'bi-info-circle-fill ws-text-blue'
        };

        const toastEl = document.createElement('div');
        toastEl.className = 'toast align-items-center border shadow-sm show';
        toastEl.id = toastId;
        toastEl.setAttribute('role', 'alert');
        toastEl.setAttribute('aria-live', 'assertive');
        toastEl.setAttribute('aria-atomic', 'true');
        toastEl.style.minWidth = '280px';
        toastEl.style.backgroundColor = 'var(--ws-bg-surface-1)';
        toastEl.style.color = 'var(--ws-text-primary)';
        toastEl.style.borderRadius = 'var(--ws-radius-md)';
        toastEl.style.borderColor = 'var(--ws-border-subtle)';

        toastEl.innerHTML = `
            <div class="d-flex">
                <div class="toast-body d-flex align-items-center gap-2 small py-2 px-3">
                    <i class="bi ${iconMap[type] || iconMap.info} fs-6"></i>
                    <span class="fw-medium">${message}</span>
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;

        container.appendChild(toastEl);
        setTimeout(() => {
            toastEl.classList.remove('show');
            setTimeout(() => toastEl.remove(), 250);
        }, 4000);
    }

    // ─── Centralized Fetch Wrapper ───
    async function request(url, options = {}) {
        const defaultHeaders = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };

        const config = {
            ...options,
            headers: {
                ...defaultHeaders,
                ...(options.headers || {})
            }
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json().catch(() => ({}));

            if (!response.ok) {
                const errorMsg = data.message || `Request failed with status ${response.status}`;
                showToast(errorMsg, 'danger');
                throw new Error(errorMsg);
            }

            return data;
        } catch (error) {
            console.error('[WareSoftAPI Error]', error);
            throw error;
        }
    }

    // ─── Auth Handlers ───
    async function login(email, password) {
        try {
            const res = await request('/api/auth/login', {
                method: 'POST',
                body: JSON.stringify({ email, password })
            });
            if (res.success) {
                showToast('Authentication successful. Redirecting...', 'success');
                setTimeout(() => {
                    window.location.href = res.redirect || '/projects';
                }, 500);
            }
            return res;
        } catch (err) {
            // Handled in request
        }
    }

    async function logout() {
        try {
            const res = await request('/api/auth/logout', { method: 'POST' });
            if (res.success) {
                window.location.href = res.redirect || '/login';
            }
        } catch (err) {
            window.location.href = '/login';
        }
    }

    // ─── UI Listeners ───
    document.addEventListener('DOMContentLoaded', () => {
        // Mobile Sidebar or Public Drawer Toggle
        const toggleBtn = document.getElementById('sidebarToggle');
        const closeBtn = document.getElementById('sidebarCloseBtn');
        const sidebar = document.getElementById('appSidebar');
        const mobilePublicNav = document.getElementById('mobilePublicNav');

        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                if (sidebar) {
                    sidebar.classList.toggle('d-none');
                } else if (mobilePublicNav) {
                    mobilePublicNav.classList.toggle('d-none');
                }
            });
        }
        if (closeBtn && sidebar) {
            closeBtn.addEventListener('click', () => {
                sidebar.classList.add('d-none');
            });
        }

        // Dashboard Command Search (Cmd+K / Filterable Quick Jump)
        const cmdInput = document.getElementById('workspaceCmdInput');
        const cmdResults = document.getElementById('workspaceCmdResults');
        if (cmdInput && cmdResults) {
            cmdInput.addEventListener('focus', () => cmdResults.classList.remove('d-none'));
            cmdInput.addEventListener('input', () => {
                const q = cmdInput.value.trim().toLowerCase();
                cmdResults.classList.remove('d-none');
                cmdResults.querySelectorAll('.jp-cmd-item').forEach(item => {
                    const match = !q || item.innerText.toLowerCase().includes(q) || (item.dataset.terms || '').includes(q);
                    item.classList.toggle('d-none', !match);
                });
            });
            document.addEventListener('click', (e) => {
                if (!e.target.closest('.jp-cmd-wrap')) {
                    cmdResults.classList.add('d-none');
                }
            });
            document.addEventListener('keydown', (e) => {
                if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
                    e.preventDefault();
                    cmdInput.focus();
                } else if (e.key === 'Escape') {
                    cmdResults.classList.add('d-none');
                    cmdInput.blur();
                }
            });
        }
    });

    return {
        fetch: request,
        showToast,
        login,
        logout
    };
})();

window.WareSoftAPI = WareSoftAPI;

window.selectClusterRegion = function(label, zone) {
    const el = document.getElementById('activeRegionLabel');
    if (el) el.textContent = label;
    WareSoftAPI.showToast(`Switched active cluster edge to ${label} (${zone})`, 'info');
};
