import unittest
from unittest.mock import MagicMock, patch
import json
import os

from agent import InputError
from api.solve import analyze_payload, solve_exercise_payload, solve_payload
from api.tutor import ask_tutor_serverless
from tutor_contract import MAX_OUTPUT_TOKENS
from api import tutor as tutor_module


class VercelApiTests(unittest.TestCase):
    def test_exact_solution_and_production_flag(self):
        result = solve_payload({"A": [[2, 1], [1, 1]], "B": [5, 3], "production": True, "variables": ["Línea A", "Línea B"]})
        self.assertEqual(result["status"], "unique")
        self.assertEqual(result["solution"], ["2", "1"])
        self.assertEqual(result["max_error"], "0")
        self.assertTrue(result["production"])
        self.assertEqual(result["variables"], ["Línea A", "Línea B"])
        self.assertIn("Línea A", " ".join(result["interpretation"]))

    def test_singular_system(self):
        result = solve_payload({"A": [[1, 1], [2, 2]], "B": [1, 3]})
        self.assertEqual(result["status"], "inconsistent")
        self.assertEqual(result["rank_A"], 1)
        self.assertEqual(result["rank_augmented"], 2)

    def test_written_exercise_endpoint(self):
        result = solve_exercise_payload({"exercise": "2x + y = 5; x - y = 1"})
        self.assertEqual(result["analysis"]["solution"], ["2", "1"])
        self.assertEqual(result["variables"], ["x", "y"])

    def test_rejects_invalid_payload(self):
        for payload in (None, [], {}, {"A": [[1]], "B": [1], "production": "yes"}):
            with self.subTest(payload=payload), self.assertRaises(InputError):
                solve_payload(payload)

    @patch("api.tutor.urlopen")
    def test_tutor_recalculates_context_and_hides_key(self, urlopen):
        response = MagicMock()
        response.read.return_value = json.dumps({
            "model": "test-model", "status": "completed",
            "output": [{"type": "message", "content": [{"type": "output_text", "text": json.dumps({
                "resumen": "La solución es {{x1}}.", "pasos": [],
                "conclusion": "El cálculo proviene del motor.", "fuera_de_tema": False,
            })}]}],
            "usage": {"input_tokens": 10, "output_tokens": 4},
        }).encode()
        response.headers = {"x-request-id": "req_test"}
        urlopen.return_value.__enter__.return_value = response
        payload = {"A": [[2, 1], [1, -1]], "B": [5, 1], "production": False, "question": "¿Qué significa?", "history": []}
        report = analyze_payload(payload)
        with patch.dict(os.environ, {"OPENAI_API_KEY": "secret-test-key", "OPENAI_MODEL": "test-model"}, clear=False):
            answer = ask_tutor_serverless(report, payload, "test-client")
        self.assertEqual(answer["answer"]["resumen"], "La solución es {{x1}}.")
        self.assertEqual(answer["source"], "model")
        request = urlopen.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "Bearer secret-test-key")
        body = json.loads(request.data.decode())
        self.assertNotIn("secret-test-key", request.data.decode())
        self.assertEqual(body["text"]["format"]["type"], "json_schema")
        self.assertTrue(body["text"]["format"]["strict"])
        self.assertEqual(body["max_output_tokens"], MAX_OUTPUT_TOKENS)
        self.assertIn('"solution":["2","1"]', body["input"][0]["content"])
        self.assertNotIn("history", request.data.decode())

    @patch("api.tutor.urlopen")
    def test_invalid_model_output_retries_once_then_falls_back(self, urlopen):
        payload = {"A": [[2, 1], [1, -1]], "B": [5, 1], "question": "Explícame la solución", "method": "gauss", "step_index": 0}
        report = analyze_payload(payload)
        malformed = ("{bad json", json.dumps({"resumen": "La respuesta es 999.", "pasos": [], "conclusion": "", "fuera_de_tema": False}))
        responses = []
        for text in malformed:
            response = MagicMock()
            response.read.return_value = json.dumps({"status": "completed", "output_text": text, "usage": {"input_tokens": 5, "output_tokens": 5}}).encode()
            responses.append(response)
        urlopen.return_value.__enter__.side_effect = responses
        with patch.dict(os.environ, {"OPENAI_API_KEY": "fake-key"}), patch.object(tutor_module, "_reserve_request"):
            answer = ask_tutor_serverless(report, payload, "retry-test")
        self.assertEqual(answer["source"], "engine")
        self.assertIn("Revisemos juntos", answer["answer"]["resumen"])
        self.assertEqual(urlopen.call_count, 2)

    @patch("api.tutor.urlopen")
    def test_timeout_uses_engine_without_visible_error(self, urlopen):
        payload = {"A": [[2, 1], [1, -1]], "B": [5, 1], "question": "Ayúdame", "method": "gauss", "step_index": 0}
        urlopen.side_effect = TimeoutError("secret timeout")
        with patch.dict(os.environ, {"OPENAI_API_KEY": "fake-key"}), patch.object(tutor_module, "_reserve_request"):
            answer = ask_tutor_serverless(analyze_payload(payload), payload, "timeout-test")
        self.assertEqual(answer["source"], "engine")
        self.assertNotIn("secret", str(answer))

    def test_general_method_question_falls_back_to_complete_trace(self):
        payload = {"A": [[2, 1], [1, -1]], "B": [5, 1], "question": "Explícame Gauss completo", "method": "gauss"}
        report = analyze_payload(payload)
        with patch.dict(os.environ, {}, clear=True):
            answer = ask_tutor_serverless(report, payload, "full-trace-test")
        self.assertEqual(answer["source"], "engine")
        self.assertEqual(len(answer["answer"]["pasos"]), len(report.methods["gauss"].steps))

    def test_minute_limit_is_enforced(self):
        with patch.dict(os.environ, {"OPENAI_DAILY_REQUEST_LIMIT": "30"}):
            for _ in range(5):
                tutor_module._reserve_request("minute-test-unique")
            with self.assertRaisesRegex(Exception, "por minuto"):
                tutor_module._reserve_request("minute-test-unique")


if __name__ == "__main__":
    unittest.main()
