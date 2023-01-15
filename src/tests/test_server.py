import unittest
from prometheus_client.core import CollectorRegistry
from prometheus_client import Counter

from src.server import app


class TestFlaskPrometheus(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.registry = CollectorRegistry()

    def test_hello(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Hello World!")

        c = Counter('python_request_operations_total', 'The total number of processed requests', registry=self.registry)
        c.inc()
        self.assertEqual(c._value._value, 1)

    def test_metrics(self):
        response = self.app.get("/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/plain")

if __name__ == "__main__":
    unittest.main()
