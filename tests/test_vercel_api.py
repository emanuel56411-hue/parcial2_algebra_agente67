import unittest
from unittest.mock import MagicMock, patch
import json
import os

from agent import InputError
from api.solve import analyze_payload, solve_payload
from api.tutor import ask_tutor_serverless


class VercelApiTests(unittest.TestCase):
    def test_exact_solution_and_production_flag(self):
        result = solve_payload({"A": [[2, 1], [1, 1]], "B": [5, 3], "production": True})
        self.assertEqual(result["status"], "unique")
        self.assertEqual(result["solution"], ["2", "1"])
        self.assertEqual(result["max_error"], "0")
        self.assertTrue(result["production"])

    def test_singular_system(self):
        result = solve_payload({"A": [[1, 1], [2, 2]], "B": [1, 3]})
        self.assertEqual(result["status"], "inconsistent")
        self.assertEqual(result["rank_A"], 1)
        self.assertEqual(result["rank_augmented"], 2)

    def test_rejects_invalid_payload(self):
        for payload in (None, [], {}, {"A": [[1]], "B": [1], "production": "yes"}):
            with self.subTest(payload=payload), self.assertRaises(InputError):
                solve_payload(payload)

    @patch("api.tutor.urlopen")
    def test_tutor_recalculates_context_and_hides_key(self, urlopen):
        response = MagicMock()
        response.read.return_value = json.dumps({
            "model": "test-model", "status": "completed",
            "output": [{"type": "message", "content": [{"type": "output_text", "text": "Explicación exacta."}]}],
            "usage": {"input_tokens": 10, "output_tokens": 4},
        }).encode()
        response.headers = {"x-request-id": "req_test"}
        urlopen.return_value.__enter__.return_value = response
        payload = {"A": [[2, 1], [1, -1]], "B": [5, 1], "production": False, "question": "¿Qué significa?", "history": []}
        report = analyze_payload(payload)
        with patch.dict(os.environ, {"OPENAI_API_KEY": "secret-test-key", "OPENAI_MODEL": "test-model"}, clear=False):
            answer = ask_tutor_serverless(report, payload, "test-client")
        self.assertEqual(answer["answer"], "Explicación exacta.")
        request = urlopen.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "Bearer secret-test-key")
        body = json.loads(request.data.decode())
        self.assertNotIn("secret-test-key", request.data.decode())
        self.assertIn('"solution":["2","1"]', body["input"][0]["content"])


if __name__ == "__main__":
    unittest.main()
