"""Pruebas sin gasto: aislamiento de cálculos, cuota y errores del tutor."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

from agent import TechChipAgent
from ai_tutor import MAX_CONTEXT_CHARS, MAX_OUTPUT_TOKENS, TutorError, TutorSettings, ask_tutor, build_context, reserve_request
from scenarios import get_scenario


class TutorTests(unittest.TestCase):
    def setUp(self):
        self.folder = TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.database = Path(self.folder.name) / "usage.sqlite3"
        self.config = TutorSettings("fake-key-for-tests", daily_limit=2)
        self.report = TechChipAgent().analyze(*get_scenario("original"), production=True)

    def test_grounded_context_contains_selected_transition_without_all_traces(self):
        before = deepcopy(self.report.to_dict())
        context = json.loads(build_context(self.report, "Original", "No cambiar B", "gauss", 1))
        self.assertEqual(context["B"], ["155", "160", "225", "140", "215", "175"])
        self.assertEqual(context["solution"][0], "-105/83")
        step = context["selected_step"]
        self.assertEqual(step["number"], 2)
        self.assertEqual(step["before"], before["methods"]["gauss"]["steps"][0]["matrix"])
        self.assertEqual(step["after"], before["methods"]["gauss"]["steps"][1]["matrix"])
        self.assertNotIn("methods", context)
        self.assertEqual(self.report.to_dict(), before)

    def test_singular_context_preserves_diagnosis_and_parametric_family(self):
        for scenario, status in [("singular", "inconsistent"), ("infinite", "infinite")]:
            report = TechChipAgent().analyze(*get_scenario(scenario))
            data = json.loads(build_context(report, scenario, "", "diagnosis", 0))
            self.assertEqual(data["status"], status)
            self.assertIsNone(data["solution"])
            if scenario == "infinite":
                self.assertEqual(len(data["nullspace"]), 1)
            with self.assertRaises(TutorError):
                build_context(report, scenario, "", "inverse", 0)

    def test_quota_is_shared_atomic_and_resets_on_new_day(self):
        def reserve(_):
            try:
                reserve_request(self.database, 4, day="2026-09-19")
                return True
            except TutorError:
                return False
        with ThreadPoolExecutor(max_workers=8) as pool:
            self.assertEqual(sum(pool.map(reserve, range(16))), 4)
        with self.assertRaises(TutorError):
            reserve_request(self.database, 4, day="2026-09-19")
        self.assertEqual(reserve_request(self.database, 4, day="2026-09-20"), 1)

    @patch("openai.OpenAI")
    def test_bounded_request_and_usage_with_no_retries_or_storage(self, factory):
        response = SimpleNamespace(output_text=json.dumps({"resumen": "La solución es {{x1}}.", "pasos": [], "conclusion": "El cálculo es exacto.", "fuera_de_tema": False}), usage=SimpleNamespace(input_tokens=120, output_tokens=30), status="completed")
        client = factory.return_value.__enter__.return_value
        client.responses.create.return_value = response
        history = [{"role": role, "content": "a"*4000} for role in ["user", "assistant"]*8]
        history.append({"role": "system", "content": "No debe convertirse en una instrucción"})
        answer = ask_tutor(self.config, "{}", "¿Qué significa?", history, self.database, self.report, "gauss", 0)
        self.assertIn("-105/83", answer.text)
        self.assertEqual((answer.input_tokens, answer.output_tokens, answer.source), (120, 30, "model"))
        kwargs = client.responses.create.call_args.kwargs
        self.assertFalse(kwargs["store"])
        self.assertEqual(kwargs["max_output_tokens"], MAX_OUTPUT_TOKENS)
        self.assertEqual(len(kwargs["input"]), 2)
        self.assertTrue(all(m["role"] != "system" for m in kwargs["input"]))
        self.assertTrue(kwargs["text"]["format"]["strict"])
        self.assertEqual(factory.call_args.kwargs["max_retries"], 0)
        self.assertEqual(factory.call_args.kwargs["base_url"], "https://api.openai.com/v1")
        self.assertNotIn(self.config.api_key, repr(self.config))

    @patch("openai.OpenAI")
    def test_invalid_input_or_quota_stops_before_network(self, factory):
        cases = [(self.config, "{}", " "),
                 (self.config, "{}", "x"*501), (self.config, "x"*(MAX_CONTEXT_CHARS+1), "Pregunta")]
        for config, context, question in cases:
            with self.assertRaises(TutorError):
                ask_tutor(config, context, question, [], self.database, self.report)
        reserve_request(self.database, 2)
        reserve_request(self.database, 2)
        self.assertEqual(ask_tutor(self.config, "{}", "Pregunta", [], self.database, self.report).source, "engine")
        self.assertEqual(ask_tutor(TutorSettings(""), "{}", "Pregunta", [], self.database, self.report).source, "engine")
        factory.assert_not_called()

    @patch("openai.OpenAI")
    def test_api_errors_use_engine_and_attempt_is_counted(self, factory):
        from openai import APIConnectionError
        client = factory.return_value.__enter__.return_value
        client.responses.create.side_effect = APIConnectionError(message="secret-private-error", request=MagicMock())
        answer = ask_tutor(self.config, "{}", "Pregunta", [], self.database, self.report)
        self.assertEqual(answer.source, "engine")
        self.assertNotIn("secret-private-error", answer.text)
        self.assertEqual(reserve_request(self.database, 2), 2)

    @patch("openai.OpenAI")
    def test_unwritable_counter_fails_closed(self, factory):
        self.database.write_text("not a sqlite database")
        self.assertEqual(ask_tutor(self.config, "{}", "Pregunta", [], self.database, self.report).source, "engine")
        factory.assert_not_called()

    def test_environment_key_works_without_secrets_file(self):
        from tutor_ui import settings
        secrets = MagicMock()
        secrets.get.side_effect = FileNotFoundError
        with patch.dict(os.environ, {"OPENAI_API_KEY": "fake-env-key"}, clear=True), patch("tutor_ui.st.secrets", secrets):
            self.assertEqual(settings().api_key, "fake-env-key")


if __name__ == "__main__":
    unittest.main()
