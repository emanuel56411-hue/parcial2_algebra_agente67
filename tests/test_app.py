"""Recorridos reales de widgets con Streamlit AppTest."""
from pathlib import Path
import unittest
from streamlit.testing.v1 import AppTest

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


if __name__ == "__main__":
    unittest.main()
