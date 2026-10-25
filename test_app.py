"""Check the public HTTP contract without starting a server."""
import unittest
from app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_contract(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'service': 'docker-github-lab',
            'message': 'Hello from Docker & GitHub Lab!',
        })

    def test_health_contract(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'ok'})

    def test_missing_route(self):
        self.assertEqual(self.client.get('/missing').status_code, 404)

    def test_routes_do_not_accept_posts(self):
        for path in ('/', '/health'):
            with self.subTest(path=path):
                self.assertEqual(self.client.post(path).status_code, 405)


if __name__ == '__main__':
    unittest.main()
