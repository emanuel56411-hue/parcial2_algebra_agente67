"""Contrato del tutor y respuestas adversarias sin llamadas a OpenAI."""
from copy import deepcopy
import json
import unittest

from agent import TechChipAgent
from tutor_contract import (
    InvalidTutorOutput, RESPONSE_FORMAT, engine_answer, marker_exists,
    render_plain, validate_model_answer, validate_question,
)


class TutorContractTests(unittest.TestCase):
    @staticmethod
    def report(size, state="unique"):
        matrix = [[int(row == column) for column in range(size)] for row in range(size)]
        right = list(range(1, size + 1))
        if state != "unique":
            matrix[-1] = [0] * size
            right[-1] = int(state == "inconsistent")
        return TechChipAgent().analyze(matrix, right)

    @staticmethod
    def response(**changes):
        answer = {"resumen": "La solución es {{x1}} y el determinante es {{det}}.",
                  "pasos": [{"titulo": "Revisemos el paso", "que": "Usamos {{matriz:paso1}}.",
                             "por_que": "El cálculo procede del motor.", "ref_paso": 1}],
                  "conclusion": "El rango es {{rango_A}}.", "fuera_de_tema": False}
        answer.update(changes)
        return answer

    def test_strict_schema_and_exact_markers_for_all_sizes_and_statuses(self):
        self.assertTrue(RESPONSE_FORMAT["strict"])
        self.assertEqual(RESPONSE_FORMAT["type"], "json_schema")
        for size in (2, 3, 6):
            for state in ("unique", "infinite", "inconsistent"):
                with self.subTest(size=size, state=state):
                    report = self.report(size, state)
                    method = "gauss" if state == "unique" else "diagnosis"
                    answer = self.response()
                    if state != "unique":
                        answer["resumen"] = "El diagnóstico está en {{matriz:paso1}}."
                    self.assertEqual(validate_model_answer(json.dumps(answer), report, method), answer)
                    self.assertTrue(marker_exists("matriz:paso1", report, method))
                    self.assertTrue(marker_exists("fila:paso1:1", report, method))
                    self.assertEqual(marker_exists("x1", report, method), state == "unique")
                    engine = engine_answer(report, method, 0)
                    self.assertIn(report.diagnostic_steps[0].title if method == "diagnosis" else report.methods["gauss"].steps[0].title,
                                  render_plain(engine, report, method))
                    self.assertEqual(report.status, state)

    def test_malformed_outputs_are_rejected_and_engine_fallback_is_usable(self):
        report = self.report(2)
        cases = [
            "{bad json",
            self.response(resumen="Valor {{desconocido}}"),
            self.response(resumen="La solución es 999."),
            self.response(resumen="Texto " * 50),
            self.response(resumen="Paso 999 del cálculo"),
            self.response(resumen="La fórmula es x=2"),
            self.response(pasos=[{"titulo": "Inventado", "que": "", "por_que": "", "ref_paso": 999}]),
        ]
        for item in cases:
            with self.subTest(item=item), self.assertRaises(InvalidTutorOutput):
                validate_model_answer(item, report, "gauss")
            fallback = engine_answer(report, "gauss", 0)
            self.assertIn("Revisemos juntos", render_plain(fallback, report, "gauss"))
        answer = self.response()
        original = deepcopy(answer)
        validate_model_answer(answer, report, "gauss")
        self.assertEqual(answer, original)

    def test_question_length_and_private_data(self):
        for question in (" ", "x" * 501, "Mi correo es alguien@example.com", "Mi clave api es secreta", "sk-abcdefghi"):
            with self.subTest(question=question), self.assertRaises(ValueError):
                validate_question(question)
        self.assertEqual(validate_question("  ¿Por qué este pivote?  "), "¿Por qué este pivote?")


if __name__ == "__main__":
    unittest.main()
