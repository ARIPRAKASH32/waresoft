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
            success: 'bi-check-circle-fill text-success',
            warning: 'bi-exclamation-triangle-fill text-warning',
            danger: 'bi-x-circle-fill text-danger',
            info: 'bi-info-circle-fill text-info'
        };

        const toastEl = document.createElement('div');
        toastEl.className = 'toast align-items-center text-white bg-dark border border-secondary border-opacity-25 show';
        toastEl.id = toastId;
        toastEl.setAttribute('role', 'alert');
        toastEl.setAttribute('aria-live', 'assertive');
        toastEl.setAttribute('aria-atomic', 'true');
        toastEl.style.minWidth = '280px';
        toastEl.style.borderRadius = 'var(--ws-radius-sm)';

        toastEl.innerHTML = `
            <div class="d-flex">
                <div class="toast-body d-flex align-items-center gap-2 small py-2 px-3">
                    <i class="bi ${iconMap[type] || iconMap.info} fs-6"></i>
                    <span>${message}</span>
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
        // Mobile Sidebar Drawer Toggle
        const toggleBtn = document.getElementById('sidebarToggle');
        const closeBtn = document.getElementById('sidebarCloseBtn');
        const sidebar = document.getElementById('appSidebar');

        if (toggleBtn && sidebar) {
            toggleBtn.addEventListener('click', () => {
                sidebar.classList.toggle('d-none');
            });
        }
        if (closeBtn && sidebar) {
            closeBtn.addEventListener('click', () => {
                sidebar.classList.add('d-none');
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
