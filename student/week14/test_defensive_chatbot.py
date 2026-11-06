"""Ordinary local functionality tests; no attack or extraction payloads."""
import unittest
from unittest.mock import patch
from markupsafe import Markup

from defensive_chatbot import app, MAX_MESSAGE_CHARS, MAX_REPLY_CHARS


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_and_greeting(self):
        self.assertIn(b"Ask me something!", self.client.get("/").data)
        response = self.client.get("/", query_string={"msg": "hello"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello!", response.data)

    def test_plain_text_and_unicode(self):
        response = self.client.get("/", query_string={"msg": "Tea & coffee: 2 < 3; สวัสดี"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Tea &amp; coffee: 2 &lt; 3; สวัสดี", response.get_data(as_text=True))

    def test_model_output_is_escaped(self):
        with patch("defensive_chatbot.mock_llm", return_value="2 < 3 & 4 > 1"):
            response = self.client.get("/", query_string={"msg": "Compare numbers"})
        self.assertIn(b"2 &lt; 3 &amp; 4 &gt; 1", response.data)

    def test_input_boundaries(self):
        self.assertEqual(self.client.get("/", query_string={"msg": "a" * MAX_MESSAGE_CHARS}).status_code, 200)
        for query in ({"msg": "a" * (MAX_MESSAGE_CHARS + 1)},
                      [("msg", "tea"), ("msg", "coffee")],
                      {"extra": "tea"}, {"msg": "tea\x00"}):
            with self.subTest(query_type=type(query).__name__):
                with patch("defensive_chatbot.mock_llm") as model:
                    self.assertEqual(self.client.get("/", query_string=query).status_code, 400)
                    model.assert_not_called()
        self.assertEqual(self.client.get("/?msg=" + "a" * 8193).status_code, 413)
        self.assertIn(b"Ask me something!", self.client.get("/", query_string={"msg": "   "}).data)

    def test_response_headers(self):
        for url in ("/", "/?extra=tea"):
            response = self.client.get(url)
            self.assertIn("default-src 'none'", response.headers["Content-Security-Policy"])
            self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
            self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_model_output_contract(self):
        for output in (None, {"answer": "tea"}, Markup("2 < 3 & 4 > 1"),
                       "a" * (MAX_REPLY_CHARS + 1)):
            with self.subTest(output_type=type(output).__name__):
                with patch("defensive_chatbot.mock_llm", return_value=output):
                    response = self.client.get("/", query_string={"msg": "Compare numbers"})
                self.assertEqual(response.status_code, 502)
                self.assertIn(b"Unable to display this response.", response.data)
                self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_model_output_size_boundary(self):
        with patch("defensive_chatbot.mock_llm", return_value="a" * MAX_REPLY_CHARS):
            response = self.client.get("/", query_string={"msg": "tea"})
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
