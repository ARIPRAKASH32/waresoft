# WareSoft (DevNexus)

**Software Delivery Operating System** — Unified Enterprise Services & Lifecycle Management Platform

WareSoft consolidates 18 lifecycle capabilities into **8 calm, tabbed workspaces** using a Juspay-inspired Blend Design System (`#FFFFFF` / `#F8FAFC` surfaces, `#0B1020` ink, `#3B82F6` blue, `#06B6D4` cyan, Plus Jakarta Sans + Inter + JetBrains Mono).

## 8 Unified Workspaces
1. **Public Showcase (`/`)** — Hero with Three.js 3D topology fabric, hairline stat strip, interactive 4-phase lifecycle switcher, and architecture brief form.
2. **Identity Portal (`/auth`)** — Unified Sign In, Organization Registration, and Password Recovery.
3. **Command & Analytics Center (`/admin`)** — Executive overview, Clients & RBAC directory, and Sprint Velocity analytics.
4. **Client & Commercial (`/client`)** — Active sprint summary, Requirements ledger, 3-step RFP submission, Quotations & digital sign-off, and MSA compliance.
5. **Projects & Delivery Studio (`/projects`)** — Filterable Projects Directory, 5-lane drag-and-drop Sprint Kanban, Milestones & Escrow, Task Backlog, and Team Bandwidth.
6. **Engineering & QA Cockpit (`/developer`)** — Personal Sprint tasks, GitHub PR & commit tracker, Defect tracker, and Test suite coverage.
7. **Cloud Ops, SLA & Billing (`/operations`)** — CI/CD deployment console, Release history, SLA support tickets, and Milestone escrow invoices.
8. **Account & Alerts (`/account`)** — User preferences, 2FA security, and real-time notification stream.

*(All 35+ legacy deep links route cleanly to their corresponding unified workspace tab via `active_tab`.)*

## Running Locally & Verifying Tests
```bash
source .venv/bin/activate
python app.py
.venv/bin/python -m unittest frontend/tests/test_routes.py -v
```
