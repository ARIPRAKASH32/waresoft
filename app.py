import os
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'frontend', 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), 'frontend', 'static'),
    static_url_path='/static'
)
app.secret_key = os.environ.get('SECRET_KEY', 'waresoft-devnexus-secret-key-2026')

# -------------------------------------------------------------
# Global Template Context
# -------------------------------------------------------------
@app.context_processor
def inject_global_data():
    return {
        'app_name': 'WareSoft',
        'platform_codename': 'DevNexus',
        'current_user': session.get('user', {
            'name': 'Ari Prakash',
            'email': 'ariprakash32@gmail.com',
            'role': 'Frontend Lead & Designer',
            'avatar': 'AP',
            'active_project': 'DevNexus Core Delivery'
        }),
        'system_status': {
            'env': 'PROD',
            'version': 'v2.4.1',
            'commit': '8f12a4',
            'uptime': '99.98%'
        }
    }

# -------------------------------------------------------------
# Public Website Routes
# -------------------------------------------------------------
@app.route('/')
def home():
    return render_template('public/home.html', title='Software Services & Project Delivery Platform')

@app.route('/about')
def about():
    return render_template('public/about.html', title='About WareSoft')

@app.route('/services')
def services():
    return render_template('public/services.html', title='Services & Engineering Capabilities')

@app.route('/portfolio')
def portfolio():
    return render_template('public/portfolio.html', title='Portfolio & Case Studies')

@app.route('/contact')
def contact():
    return render_template('public/contact.html', title='Contact Our Engineering Team')

@app.route('/careers')
def careers():
    return render_template('public/careers.html', title='Careers & Open Positions')

# -------------------------------------------------------------
# Authentication Routes
# -------------------------------------------------------------
@app.route('/login')
def login():
    return render_template('auth/login.html', title='Sign In - DevNexus')

@app.route('/register')
def register():
    return render_template('auth/register.html', title='Create Account - DevNexus')

@app.route('/forgot-password')
def forgot_password():
    return render_template('auth/forgot_password.html', title='Reset Password - DevNexus')

@app.route('/profile')
def profile():
    return render_template('auth/profile.html', title='User Profile & Preferences')

# -------------------------------------------------------------
# Admin Routes
# -------------------------------------------------------------
@app.route('/admin')
def admin_dashboard():
    return render_template('admin/dashboard.html', title='Admin Command Center')

@app.route('/admin/users')
def admin_users():
    return render_template('admin/users.html', title='User Directory & RBAC')

@app.route('/admin/clients')
def admin_clients():
    return render_template('admin/clients.html', title='Enterprise Client Accounts')

@app.route('/admin/analytics')
def admin_analytics():
    return render_template('admin/analytics.html', title='Platform Performance & Velocity')

# -------------------------------------------------------------
# Client Portal Routes
# -------------------------------------------------------------
@app.route('/client')
def client_dashboard():
    return render_template('client/dashboard.html', title='Client Workspace')

@app.route('/client/profile')
def client_profile():
    return render_template('client/profile.html', title='Client Organization Profile')

# -------------------------------------------------------------
# Requirements & Quotations
# -------------------------------------------------------------
@app.route('/requirements/submit')
def requirement_submit():
    return render_template('client/requirements_submit.html', title='Submit Project Requirement')

@app.route('/requirements')
def requirements_list():
    return render_template('client/requirements_list.html', title='Track Requirements & RFPs')

@app.route('/requirements/<int:req_id>')
def requirement_detail(req_id):
    return render_template('client/requirement_detail.html', req_id=req_id, title=f'Requirement RFP-#{req_id:04d}')

@app.route('/quotations')
def quotations_list():
    return render_template('client/quotations_list.html', title='Quotations & Proposals')

@app.route('/quotations/<int:quote_id>')
def quotation_detail(quote_id):
    return render_template('client/quotation_detail.html', quote_id=quote_id, title=f'Quotation QT-#{quote_id:04d}')

@app.route('/quotations/<int:quote_id>/approval')
def quotation_approval(quote_id):
    return render_template('client/quotation_approval.html', quote_id=quote_id, title=f'Approve Quotation QT-#{quote_id:04d}')

# -------------------------------------------------------------
# Project Management & Delivery Routes
# -------------------------------------------------------------
@app.route('/projects')
def projects_dashboard():
    return render_template('projects/dashboard.html', title='Project Portfolio')

@app.route('/projects/<int:project_id>')
def project_detail(project_id):
    return render_template('projects/detail.html', project_id=project_id, title=f'Project NX-#{project_id:03d}')

@app.route('/projects/<int:project_id>/milestones')
def project_milestones(project_id):
    return render_template('projects/milestones.html', project_id=project_id, title='Milestones & Gantt Timeline')

@app.route('/projects/<int:project_id>/kanban')
def project_kanban(project_id):
    return render_template('projects/kanban.html', project_id=project_id, title='Sprint Kanban Board')

@app.route('/projects/<int:project_id>/tasks')
def project_tasks(project_id):
    return render_template('projects/tasks.html', project_id=project_id, title='Task Backlog & Prioritization')

@app.route('/projects/<int:project_id>/team')
def project_team(project_id):
    return render_template('projects/team.html', project_id=project_id, title='Team Allocation & Workload')

# -------------------------------------------------------------
# Developer & GitHub Integration
# -------------------------------------------------------------
@app.route('/developer')
def developer_dashboard():
    return render_template('developer/dashboard.html', title='Developer Workspace')

@app.route('/developer/github')
def developer_github():
    return render_template('developer/github.html', title='GitHub Repositories & PR Tracker')

# -------------------------------------------------------------
# QA & Deployment
# -------------------------------------------------------------
@app.route('/qa')
def qa_dashboard():
    return render_template('qa/dashboard.html', title='Quality Assurance Hub')

@app.route('/qa/bugs')
def qa_bugs():
    return render_template('qa/bugs.html', title='Defect & Bug Tracking')

@app.route('/qa/test-cases')
def qa_test_cases():
    return render_template('qa/test_cases.html', title='Test Suites & Coverage')

@app.route('/deployment')
def deployment_dashboard():
    return render_template('deployment/dashboard.html', title='CI/CD Deployment Console')

@app.route('/deployment/releases')
def deployment_releases():
    return render_template('deployment/releases.html', title='Release History & Changelogs')

# -------------------------------------------------------------
# Maintenance, Invoices & Notifications
# -------------------------------------------------------------
@app.route('/maintenance')
def maintenance_list():
    return render_template('maintenance/list.html', title='SLA Maintenance & Support Tickets')

@app.route('/maintenance/<int:ticket_id>')
def maintenance_detail(ticket_id):
    return render_template('maintenance/detail.html', ticket_id=ticket_id, title=f'Support Ticket #{ticket_id:04d}')

@app.route('/billing')
def billing_list():
    return render_template('billing/invoices.html', title='Billing & Invoices')

@app.route('/billing/<int:invoice_id>')
def billing_detail(invoice_id):
    return render_template('billing/invoice_detail.html', invoice_id=invoice_id, title=f'Invoice INV-#{invoice_id:04d}')

@app.route('/notifications')
def notifications_center():
    return render_template('notifications/center.html', title='Notification Stream')

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
            'active_project': 'DevNexus Core Delivery'
        }
        return jsonify({'success': True, 'redirect': '/projects/101'})
    return jsonify({'success': False, 'message': 'Invalid credentials provided'}), 400

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    session.pop('user', None)
    return jsonify({'success': True, 'redirect': '/login'})

@app.route('/api/requirements', methods=['GET', 'POST'])
def api_requirements():
    if request.method == 'POST':
        payload = request.get_json() or {}
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
            {'id': 1039, 'title': 'Healthcare HIPAA Portal Redesign', 'client': 'Aegis Medical', 'budget': '$32,000', 'status': 'Proposal Sent', 'priority': 'Medium', 'created_at': '2026-11-15'}
        ]
    })

@app.route('/api/kanban/tasks', methods=['GET', 'POST', 'PUT'])
def api_kanban_tasks():
    return jsonify({
        'columns': {
            'backlog': [
                {'id': 'T-204', 'title': 'Implement Webhook Retry Exponential Backoff', 'priority': 'high', 'assignee': 'AP', 'tags': ['backend', 'reliability'], 'points': 5},
                {'id': 'T-209', 'title': 'Optimize Jinja2 SSR Cache Headers', 'priority': 'medium', 'assignee': 'AP', 'tags': ['frontend', 'perf'], 'points': 3}
            ],
            'in_progress': [
                {'id': 'T-198', 'title': 'Design Tokens & 4px Spacing Normalization', 'priority': 'critical', 'assignee': 'AP', 'tags': ['ui/ux', 'design-system'], 'points': 8},
                {'id': 'T-201', 'title': 'Three.js Service Topology Visualizer', 'priority': 'high', 'assignee': 'AP', 'tags': ['3d', 'webgl'], 'points': 8}
            ],
            'code_review': [
                {'id': 'T-195', 'title': 'Role Based Middleware for Admin Dashboard', 'priority': 'high', 'assignee': 'Datcha', 'tags': ['security', 'auth'], 'points': 5}
            ],
            'qa_testing': [
                {'id': 'T-190', 'title': 'Stripe & Razorpay Escrow Webhook Verification', 'priority': 'critical', 'assignee': 'QA Lead', 'tags': ['qa', 'billing'], 'points': 5}
            ],
            'completed': [
                {'id': 'T-185', 'title': 'Project Inception & Architecture Blueprint', 'priority': 'low', 'assignee': 'AP', 'tags': ['architecture'], 'points': 3}
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
        'message': f'Build triggered for {env} from commit 8f12a4'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
