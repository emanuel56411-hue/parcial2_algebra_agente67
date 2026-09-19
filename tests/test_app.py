"""Recorridos reales de widgets con Streamlit AppTest."""
from pathlib import Path
import unittest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
from ai_tutor import TutorAnswer, TutorError, TutorSettings

APP = Path(__file__).resolve().parents[1] / "app.py"


class AppTests(unittest.TestCase):
    def app(self):
        at = AppTest.from_file(str(APP), default_timeout=20).run()
        self.assertFalse(at.exception)
        return at

    def solve(self, at):
        next(b for b in at.button if b.label == "Resolver sistema").click().run()
        self.assertFalse(at.exception)
        return at

    def test_original_and_method_navigation(self):
        at = self.solve(self.app())
        self.assertTrue(at.warning)
        self.assertEqual(at.metric[1].value, "-83")
        for method in ["gauss", "gauss_jordan", "inverse"]:
            at.selectbox(key="method").select(method).run()
            self.assertFalse(at.exception)
            at.select_slider(key=f"step_{method}").set_value(2).run()
            self.assertFalse(at.exception)
            at.segmented_control(key=f"view_{method}").set_value("Todos los pasos").run()
            self.assertFalse(at.exception)

    def test_all_scenarios_clear_stale_results(self):
        at = self.app()
        for key, expected in [("compatible", "Solución única"), ("scarcity", "Solución única"), ("singular", "Sin solución"), ("infinite", "Infinitas soluciones"), ("example", "Solución única")]:
            at.selectbox(key="scenario").select(key).run()
            self.assertEqual(len(at.metric), 0)
            self.solve(at)
            self.assertEqual(at.metric[0].value, expected)

    def test_custom_dimension(self):
        at = self.app()
        at.segmented_control(key="source").set_value("Matriz propia").run()
        at.number_input(key="dimension").set_value(2).run()
        self.solve(at)
        self.assertEqual(at.session_state.report.solution, [1, 1])

    def test_editor_changes_are_applied(self):
        at = self.app()
        at.segmented_control(key="source").set_value("Matriz propia").run()
        at.number_input(key="dimension").set_value(2).run()
        at.session_state["editor_Matriz propia_2"] = {"edited_rows": {0: {"x1": "2", "B": "3"}}, "added_rows": [], "deleted_rows": []}
        self.solve(at)
        self.assertEqual(str(at.session_state.report.solution[0]), "3/2")

    def test_json_invalid_input_removes_old_result(self):
        at = self.app()
        at.segmented_control(key="source").set_value("Importar JSON").run()
        at.text_area(key="json_text").set_value('{"A":[["1/3"]],"B":[2]}')
        self.solve(at)
        self.assertEqual(at.session_state.report.solution, [6])
        at.text_area(key="json_text").set_value('{"A":[[1,2]],"B":[3]}')
        self.solve(at)
        self.assertTrue(at.error)
        self.assertEqual(len(at.metric), 0)

    def test_guide_and_validation_pages(self):
        at = self.app()
        at.radio(key="page").set_value("Guía de métodos").run()
        self.assertFalse(at.exception)
        at.radio(key="page").set_value("Validación del parcial").run()
        at.button[0].click().run()
        self.assertFalse(at.exception)
        self.assertTrue(at.success)
        self.assertTrue(at.session_state.validation["all_passed"])

    def test_tutor_is_optional_and_never_calls_api_without_action(self):
        with patch("tutor_ui.settings", return_value=TutorSettings("")), patch("tutor_ui.ask_tutor") as api:
            at = self.solve(self.app())
            self.assertTrue(at.chat_input(key="tutor_prompt").disabled)
            self.assertTrue(at.button(key="tutor_explain_step").disabled)
            self.assertIn("Tutor IA", [tab.label for tab in at.tabs])
            self.assertEqual(at.session_state.report.determinant, -83)
            at.run()
            api.assert_not_called()

    def test_tutor_chat_uses_current_result_and_clears_on_new_system(self):
        response = TutorAnswer("El valor negativo impide este plan de producción.", 100, 20)
        with patch("tutor_ui.settings", return_value=TutorSettings("test-key")), patch("tutor_ui.ask_tutor", return_value=response) as api:
            at = self.solve(self.app())
            api.assert_not_called()
            at.chat_input(key="tutor_prompt").set_value("¿Por qué es negativo?").run()
            self.assertFalse(at.exception)
            self.assertEqual(len(at.chat_message), 2)
            self.assertIn("-105/83", api.call_args.args[1])
            self.assertEqual(at.session_state.tutor_tokens, 120)
            at.run()
            self.assertEqual(api.call_count, 1)
            at.selectbox(key="scenario").select("compatible").run()
            self.assertNotIn("tutor_messages", at.session_state)
            self.solve(at)
            self.assertEqual(len(at.chat_message), 0)
            self.assertEqual(api.call_count, 1)

    def test_step_tutor_receives_the_selected_transition(self):
        import json
        with patch("tutor_ui.settings", return_value=TutorSettings("test-key")), patch("tutor_ui.ask_tutor", return_value=TutorAnswer("Se intercambian filas.")) as api:
            at = self.solve(self.app())
            at.selectbox(key="method").select("gauss").run()
            at.select_slider(key="step_gauss").set_value(2).run()
            api.assert_not_called()
            at.button(key="tutor_explain_step").click().run()
            self.assertFalse(at.exception)
            step = json.loads(api.call_args.args[1])["selected_step"]
            self.assertEqual((step["method"], step["number"]), ("gauss", 2))
            self.assertTrue(step["before"])
            at.select_slider(key="step_gauss").set_value(3).run()
            self.assertFalse(any(m.value == "Se intercambian filas." for m in at.markdown))
            self.assertEqual(api.call_count, 1)

    def test_tutor_failure_does_not_break_calculator(self):
        with patch("tutor_ui.settings", return_value=TutorSettings("test-key")), patch("tutor_ui.ask_tutor", side_effect=TutorError("Cuota agotada")):
            at = self.solve(self.app())
            at.chat_input(key="tutor_prompt").set_value("Explica el resultado").run()
            self.assertFalse(at.exception)
            self.assertTrue(any(error.value == "Cuota agotada" for error in at.error))
            self.assertEqual(at.session_state.report.determinant, -83)
            self.assertEqual(len(at.chat_message), 0)


if __name__ == "__main__":
    unittest.main()
