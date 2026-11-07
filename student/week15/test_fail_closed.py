"""Benign regression test for the Week 15 fail-closed teaching service."""

import importlib.util
import logging
from pathlib import Path
import unittest


SERVICE = Path(__file__).parents[2] / "labs/week15-devsecops-pipeline/sample-service.py"


def load_service():
    spec = importlib.util.spec_from_file_location("week15_sample_service", SERVICE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RaisingTokenStore:
    def get(self, _token):
        raise RuntimeError("synthetic test detail must not reach the client")


class FailClosedTest(unittest.TestCase):
    def test_unexpected_authorization_error_is_logged_and_denied(self):
        service = load_service()
        service._VALID_TOKENS = RaisingTokenStore()

        with self.assertLogs("security", logging.ERROR) as captured:
            response = service.app.test_client().get(
                "/admin", headers={"Authorization": "benign-test-token"}
            )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json(), {"error": "forbidden"})
        log_text = "\n".join(captured.output)
        self.assertIn("event=authz_error", log_text)
        self.assertIn("outcome=deny", log_text)
        self.assertIn("error=RuntimeError", log_text)
        self.assertNotIn("synthetic test detail", log_text)


if __name__ == "__main__":
    unittest.main()
