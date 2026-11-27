# WareSoft (DevNexus)

**Enterprise Software Services & Project Delivery Lifecycle Platform**

WareSoft is a unified management platform designed to orchestrate the complete software service lifecycle—from client requirements, quotations, project planning, and Kanban execution to QA, CI/CD deployment, SLA maintenance, and escrow billing.

## Technology Stack
- **Frontend Core:** HTML5, CSS3 (Custom Properties & 4px Grid Design Tokens), Bootstrap 5, ES6+ JavaScript
- **UI Architecture:** All-Light Editorial Shell (`#FFFFFF` header/sidebar, `#F4F7FB` canvas, `#0B1020` ink, `#3B82F6` blue, `#06B6D4` cyan) with split filter-sidebar & structured directory cards
- **Templates:** Python Flask Jinja2 Templates
- **Data Integration:** Asynchronous REST client (`frontend/static/js/api.js`) via native Fetch API
- **3D / Visuals:** Shaded Three.js WebGL Service Topology Visualizer (`frontend/static/js/3d-visualizer.js`)

## Modules & Routes
- **Public Website:** `/`, `/about`, `/services`, `/portfolio`, `/contact`, `/careers`
- **Authentication:** `/login`, `/register`, `/forgot-password`, `/profile`
- **Admin Center:** `/admin`, `/admin/users`, `/admin/clients`, `/admin/analytics`
- **Client & Commercial:** `/client`, `/client/profile`, `/requirements`, `/requirements/submit`, `/requirements/<id>`, `/quotations`, `/quotations/<id>`, `/quotations/<id>/approval`
- **Project Delivery:** `/projects`, `/projects/<id>`, `/projects/<id>/milestones`, `/projects/<id>/kanban`, `/projects/<id>/tasks`, `/projects/<id>/team`
- **Developer & GitHub:** `/developer`, `/developer/github`
- **QA & CI/CD:** `/qa`, `/qa/bugs`, `/qa/test-cases`, `/deployment`, `/deployment/releases`
- **Operations & Finance:** `/maintenance`, `/maintenance/<id>`, `/billing`, `/billing/<id>`, `/notifications`

## Running Locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Running Verification Tests
```bash
.venv/bin/python -m unittest frontend/tests/test_routes.py -v
```
