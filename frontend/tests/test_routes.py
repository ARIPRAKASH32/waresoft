import html as html_lib
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app import app


class WareSoftUnifiedWorkspaceTests(unittest.TestCase):
    """Verify the 8 unified workspaces, legacy route tab-mapping, and REST APIs."""

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_eight_primary_workspaces(self):
        workspaces = [
            ('/', 'Software delivery, engineered for enterprise scale.'),
            ('/auth', 'DevNexus Identity Portal'),
            ('/admin', 'Command & Analytics Center'),
            ('/client', 'Client & Commercial Workspace'),
            ('/projects', 'Projects & Delivery Studio'),
            ('/developer', 'Engineering & QA Cockpit'),
            ('/operations', 'Cloud Ops, SLA & Billing Hub'),
            ('/account', 'Account & Notifications'),
        ]
        for route, marker in workspaces:
            with self.subTest(route=route):
                resp = self.client.get(route)
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn('Manrope', html)
                self.assertNotIn('Plus+Jakarta+Sans', html)
                self.assertIn('logo.svg', html)
                self.assertIn('data-bs-theme="light"', html)
                self.assertIn(marker, html_lib.unescape(html))
                if route in ('/', '/auth'):
                    self.assertIn('Open Console', html)
                    self.assertNotIn('workspaceCmdInput', html)
                else:
                    self.assertIn('workspaceCmdInput', html)

    def test_legacy_routes_and_tab_parameters(self):
        legacy_routes = [
            '/about', '/services', '/portfolio', '/contact', '/careers',
            '/login', '/register', '/forgot-password', '/profile',
            '/admin/users', '/admin/clients', '/admin/analytics',
            '/client/profile', '/requirements/submit', '/requirements',
            '/requirements/1041', '/quotations', '/quotations/1041',
            '/quotations/1041/approval', '/projects/101', '/projects/101/kanban',
            '/projects/101/milestones', '/projects/101/tasks', '/projects/101/team',
            '/developer/github', '/qa', '/qa/bugs', '/qa/test-cases',
            '/deployment', '/deployment/releases', '/maintenance', '/maintenance/3041',
            '/billing', '/billing/2048', '/notifications',
        ]
        for route in legacy_routes:
            with self.subTest(route=route):
                resp = self.client.get(route)
                self.assertEqual(resp.status_code, 200, f'Legacy route {route} failed')

    def test_static_images_and_logo_available(self):
        for asset in ['logo.svg', 'platform-architecture.jpg', 'sprint-workflow.jpg', 'cloud-vault.jpg']:
            with self.subTest(asset=asset):
                resp = self.client.get(f'/static/images/{asset}')
                self.assertEqual(resp.status_code, 200)
                resp.close()

    def test_api_endpoints(self):
        self.assertEqual(self.client.post('/api/auth/login', json={'email': 'ari@waresoft.dev'}).status_code, 200)
        self.assertEqual(self.client.post('/api/auth/login', json={}).status_code, 400)
        self.assertEqual(self.client.post('/api/auth/logout').status_code, 200)
        self.assertEqual(self.client.get('/api/requirements').status_code, 200)
        self.assertEqual(self.client.post('/api/requirements', json={'title': 'Test'}).status_code, 201)
        self.assertEqual(self.client.get('/api/kanban/tasks').status_code, 200)
        self.assertEqual(self.client.post('/api/deployment/trigger', json={'environment': 'staging'}).status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)
