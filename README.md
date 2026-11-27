# WareSoft (DevNexus)

**Enterprise Software Services & Project Delivery Lifecycle Platform**

WareSoft is a unified management platform designed to orchestrate the complete software service lifecycle:
from client requirements, quotations, project planning, and task execution, to QA, CI/CD deployment, maintenance, and client billing.

## Technology Stack
- **Frontend Core:** HTML5, CSS3 (Custom Properties & Design Tokens), Bootstrap 5, Modern Vanilla ES6+ JavaScript
- **Templates:** Python Flask Jinja2 Templates
- **Data Integration:** Asynchronous REST client via native Fetch API with JWT/CSRF support
- **3D / Visuals:** Lightweight Three.js WebGL Architecture Visualizer

## Directory Structure
```
waresoft/
├── app.py                      # Flask development server & routing endpoints
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   ├── tokens.css      # Core design tokens, dark navy & electric blue palette
│   │   │   ├── base.css        # Reset, typography, 4px grid rhythm, layout shells
│   │   │   ├── components.css  # Data tables, kanban cards, stat metrics, badges, modals
│   │   │   └── modules/        # Module-specific stylesheets
│   │   ├── js/
│   │   │   ├── api.js          # Unified Fetch client with auth, error handling & toasts
│   │   │   ├── 3d-visualizer.js# Three.js 3D architecture canvas
│   │   │   └── modules/        # Interactive controllers (kanban, charts, wizard)
│   │   └── images/             # Vector icons & branding assets
│   ├── templates/
│   │   ├── base.html           # Unified master Jinja2 shell
│   │   ├── components/         # Reusable navigation, breadcrumbs, modals
│   │   ├── public/             # Home, About, Services, Portfolio, Contact, Careers
│   │   ├── auth/               # Login, Register, Forgot Password, Profile
│   │   ├── admin/              # Users, Clients, Platform Analytics
│   │   ├── client/             # Client Dashboard, Requirements, Quotations
│   │   ├── developer/          # Assigned Tasks, Dev Progress, GitHub View
│   │   ├── projects/           # Overview, Milestones, Kanban, Tasks, Team
│   │   ├── qa/                 # Bug Tracker, Test Suites, Run History
│   │   ├── deployment/         # Releases, CI/CD Pipeline, Environment Status
│   │   ├── maintenance/        # Support Tickets, SLAs, System Logs
│   │   ├── billing/            # Invoices, Quotation Approvals, Payment History
│   │   └── notifications/      # Notification Center & Preferences
│   └── tests/                  # Frontend test suites & verification scripts
```

## Running the Platform
```bash
source .venv/bin/activate
python app.py
```
Open `http://localhost:5000` to access the WareSoft DevNexus console.
