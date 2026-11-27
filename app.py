import os
from flask import Flask, render_template, jsonify, request, redirect, url_for, session

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'frontend', 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), 'frontend', 'static'),
    static_url_path='/static'
)
app.secret_key = os.environ.get('SECRET_KEY', 'waresoft-devnexus-secret-key-2026')


@app.context_processor
def inject_global_data():
    return {
        'app_name': 'WareSoft',
        'platform_codename': 'DevNexus',
        'current_user': session.get('user', {
            'name': 'Ari Prakash',
            'email': 'ariprakash32@gmail.com',
            'role': 'Frontend Lead',
            'avatar': 'AP',
            'active_project': 'DevNexus Core'
        }),
        'system_status': {
            'env': 'PROD',
            'version': 'v2.4.2',
            'commit': '9b10618',
            'uptime': '99.98%'
        }
    }


# -------------------------------------------------------------
# 1. Public Showcase (Unified Home + Solutions + Contact)
# -------------------------------------------------------------
@app.route('/')
@app.route('/about')
@app.route('/services')
@app.route('/portfolio')
@app.route('/contact')
@app.route('/careers')
def home():
    return render_template('public/home.html', title='Software Delivery Operating System')


# -------------------------------------------------------------
# 2. Unified Authentication Portal
# -------------------------------------------------------------
@app.route('/auth')
@app.route('/login')
def login():
    tab = request.args.get('tab', 'login')
    return render_template('auth/portal.html', active_tab=tab, title='Identity Portal')


@app.route('/register')
def register():
    return render_template('auth/portal.html', active_tab='register', title='Create Account')


@app.route('/forgot-password')
def forgot_password():
    return render_template('auth/portal.html', active_tab='forgot', title='Reset Password')


# -------------------------------------------------------------
# 3. Command & Analytics Center
# -------------------------------------------------------------
@app.route('/admin')
def admin_dashboard():
    tab = request.args.get('tab', 'overview')
    return render_template('admin/workspace.html', active_tab=tab, title='Command & Analytics')


@app.route('/admin/users')
@app.route('/admin/clients')
def admin_directory():
    return render_template('admin/workspace.html', active_tab='directory', title='Clients & Users')


@app.route('/admin/analytics')
def admin_analytics():
    return render_template('admin/workspace.html', active_tab='analytics', title='Velocity Analytics')


# -------------------------------------------------------------
# 4. Client & Commercial Workspace
# -------------------------------------------------------------
@app.route('/client')
def client_dashboard():
    tab = request.args.get('tab', 'overview')
    return render_template('client/workspace.html', active_tab=tab, title='Client & Commercial')


@app.route('/client/profile')
def client_profile():
    return render_template('client/workspace.html', active_tab='profile', title='Organization & MSA')


@app.route('/requirements/submit')
def requirement_submit():
    return render_template('client/workspace.html', active_tab='submit', title='Submit Requirement')


@app.route('/requirements')
@app.route('/requirements/<int:req_id>')
def requirements_list(req_id=None):
    return render_template('client/workspace.html', active_tab='requirements', title='Requirements Ledger')


@app.route('/quotations')
@app.route('/quotations/<int:quote_id>')
@app.route('/quotations/<int:quote_id>/approval')
def quotations_list(quote_id=None):
    return render_template('client/workspace.html', active_tab='quotes', title='Quotations & Sign-off')


# -------------------------------------------------------------
# 5. Projects & Delivery Studio
# -------------------------------------------------------------
@app.route('/projects')
@app.route('/projects/<int:project_id>')
def projects_dashboard(project_id=101):
    tab = request.args.get('tab', 'directory')
    return render_template('projects/workspace.html', project_id=project_id, active_tab=tab, title='Projects & Delivery')


@app.route('/projects/<int:project_id>/kanban')
def project_kanban(project_id):
    return render_template('projects/workspace.html', project_id=project_id, active_tab='kanban', title='Sprint Kanban')


@app.route('/projects/<int:project_id>/milestones')
def project_milestones(project_id):
    return render_template('projects/workspace.html', project_id=project_id, active_tab='milestones', title='Milestones')


@app.route('/projects/<int:project_id>/tasks')
def project_tasks(project_id):
    return render_template('projects/workspace.html', project_id=project_id, active_tab='tasks', title='Task Backlog')


@app.route('/projects/<int:project_id>/team')
def project_team(project_id):
    return render_template('projects/workspace.html', project_id=project_id, active_tab='team', title='Team Allocation')


# -------------------------------------------------------------
# 6. Engineering & QA Cockpit
# -------------------------------------------------------------
@app.route('/developer')
def developer_dashboard():
    tab = request.args.get('tab', 'sprint')
    return render_template('developer/workspace.html', active_tab=tab, title='Engineering & QA')


@app.route('/developer/github')
def developer_github():
    return render_template('developer/workspace.html', active_tab='github', title='GitHub PRs & Commits')


@app.route('/qa')
@app.route('/qa/bugs')
def qa_dashboard():
    return render_template('developer/workspace.html', active_tab='qa', title='QA & Defects')


@app.route('/qa/test-cases')
def qa_test_cases():
    return render_template('developer/workspace.html', active_tab='tests', title='Test Suites')


# -------------------------------------------------------------
# 7. Cloud Ops, SLA & Billing Hub
# -------------------------------------------------------------
@app.route('/operations')
@app.route('/deployment')
def deployment_dashboard():
    tab = request.args.get('tab', 'deployments')
    return render_template('operations/workspace.html', active_tab=tab, title='Cloud Ops & Billing')


@app.route('/deployment/releases')
def deployment_releases():
    return render_template('operations/workspace.html', active_tab='releases', title='Release History')


@app.route('/maintenance')
@app.route('/maintenance/<int:ticket_id>')
def maintenance_list(ticket_id=None):
    return render_template('operations/workspace.html', active_tab='maintenance', title='SLA Support Tickets')


@app.route('/billing')
@app.route('/billing/<int:invoice_id>')
def billing_list(invoice_id=None):
    return render_template('operations/workspace.html', active_tab='billing', title='Billing & Invoices')


# -------------------------------------------------------------
# 8. Account & Notification Stream
# -------------------------------------------------------------
@app.route('/account')
@app.route('/profile')
def profile():
    tab = request.args.get('tab', 'profile')
    return render_template('account/workspace.html', active_tab=tab, title='Account & Alerts')


@app.route('/notifications')
def notifications_center():
    return render_template('account/workspace.html', active_tab='notifications', title='Notification Stream')


# -------------------------------------------------------------
# Backend API Integration Endpoints (DevNexus Data Contract)
# -------------------------------------------------------------
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    email = data.get('email', '')
    if email:
        session['user'] = {
            'name': email.split('@')[0].capitalize(),
            'email': email,
            'role': 'Engineering Lead',
            'avatar': email[0:2].upper(),
            'active_project': 'DevNexus Core'
        }
        return jsonify({'success': True, 'redirect': '/projects'})
    return jsonify({'success': False, 'message': 'Invalid credentials provided'}), 400


@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    session.pop('user', None)
    return jsonify({'success': True, 'redirect': '/login'})


@app.route('/api/requirements', methods=['GET', 'POST'])
def api_requirements():
    if request.method == 'POST':
        return jsonify({
            'success': True,
            'id': 1042,
            'status': 'SUBMITTED',
            'message': 'Requirement RFP-1042 successfully registered.'
        }), 201
    return jsonify({
        'requirements': [
            {'id': 1041, 'title': 'Cloud Native Payment Gateway', 'client': 'FinTech Global', 'budget': '$45,000', 'status': 'Under Review', 'priority': 'High', 'created_at': '2026-11-20'},
            {'id': 1040, 'title': 'Warehouse IoT Telemetry Hub', 'client': 'Logix Logistics', 'budget': '$78,000', 'status': 'Approved', 'priority': 'Critical', 'created_at': '2026-11-18'},
        ]
    })


@app.route('/api/kanban/tasks', methods=['GET', 'POST', 'PUT'])
def api_kanban_tasks():
    return jsonify({
        'columns': {
            'backlog': [
                {'id': 'T-204', 'title': 'Webhook Retry Exponential Backoff', 'priority': 'high', 'assignee': 'AP', 'points': 5},
                {'id': 'T-209', 'title': 'Optimize Jinja2 SSR Cache Headers', 'priority': 'medium', 'assignee': 'AP', 'points': 3}
            ],
            'in_progress': [
                {'id': 'T-198', 'title': 'Blend Design Tokens & Workspace Tabs', 'priority': 'critical', 'assignee': 'AP', 'points': 8},
                {'id': 'T-201', 'title': 'Three.js Service Fabric Visualizer', 'priority': 'high', 'assignee': 'AP', 'points': 8}
            ],
            'code_review': [
                {'id': 'T-195', 'title': 'Admin RBAC Middleware', 'priority': 'high', 'assignee': 'Datcha', 'points': 5}
            ],
            'completed': [
                {'id': 'T-185', 'title': 'Architecture Blueprint & Schema', 'priority': 'low', 'assignee': 'AP', 'points': 3}
            ]
        }
    })


@app.route('/api/deployment/trigger', methods=['POST'])
def api_deploy_trigger():
    data = request.get_json() or {}
    env = data.get('environment', 'staging')
    return jsonify({
        'success': True,
        'deployment_id': 'dep-8841',
        'environment': env,
        'status': 'BUILDING',
        'message': f'Build triggered for {env} from commit 9b10618'
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
