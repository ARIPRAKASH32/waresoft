import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app import app


class WareSoftFrontendTests(unittest.TestCase):
    """Comprehensive route, template rendering, and REST API contract verification."""

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_all_page_routes_return_200(self):
        routes = [
            '/', '/about', '/services', '/portfolio', '/contact', '/careers',
            '/login', '/register', '/forgot-password', '/profile',
            '/admin', '/admin/users', '/admin/clients', '/admin/analytics',
            '/client', '/client/profile',
            '/requirements/submit', '/requirements', '/requirements/1041',
            '/quotations', '/quotations/1041', '/quotations/1041/approval',
            '/projects', '/projects/101', '/projects/101/milestones',
            '/projects/101/kanban', '/projects/101/tasks', '/projects/101/team',
            '/developer', '/developer/github',
            '/qa', '/qa/bugs', '/qa/test-cases',
            '/deployment', '/deployment/releases',
            '/maintenance', '/maintenance/3041',
            '/billing', '/billing/2048',
            '/notifications',
        ]
        for route in routes:
            with self.subTest(route=route):
                resp = self.client.get(route)
                self.assertEqual(resp.status_code, 200, f'Route {route} failed with {resp.status_code}')
                html = resp.get_data(as_text=True)
                self.assertIn('data-bs-theme="light"', html)
                self.assertIn('WareSoft', html)

    def test_api_auth_login_and_logout(self):
        resp = self.client.post('/api/auth/login', json={'email': 'ari@waresoft.dev', 'password': 'secret'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.get_json()['success'])

        bad = self.client.post('/api/auth/login', json={})
        self.assertEqual(bad.status_code, 400)

        out = self.client.post('/api/auth/logout')
        self.assertEqual(out.status_code, 200)
        self.assertTrue(out.get_json()['success'])

    def test_api_requirements_and_kanban_and_deploy(self):
        reqs = self.client.get('/api/requirements')
        self.assertEqual(reqs.status_code, 200)
        self.assertIn('requirements', reqs.get_json())

        created = self.client.post('/api/requirements', json={'title': 'Test RFP'})
        self.assertEqual(created.status_code, 201)
        self.assertTrue(created.get_json()['success'])

        kanban = self.client.get('/api/kanban/tasks')
        self.assertEqual(kanban.status_code, 200)
        self.assertIn('columns', kanban.get_json())

        deploy = self.client.post('/api/deployment/trigger', json={'environment': 'staging'})
        self.assertEqual(deploy.status_code, 200)
        self.assertEqual(deploy.get_json()['environment'], 'staging')


if __name__ == '__main__':
    unittest.main(verbosity=2)
