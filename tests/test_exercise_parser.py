"""Ejercicios escritos: conversión exacta y rechazo de expresiones inseguras."""
from fractions import Fraction
import json
from unittest.mock import MagicMock, patch
import unittest

from agent import InputError, TechChipAgent
from api.solve import solve_exercise_payload
from exercise_parser import parse_exercise
from exercise_interpreter import interpret_exercise


class ExerciseParserTests(unittest.TestCase):
    def test_symbolic_equations_are_converted_and_solved(self):
        parsed = parse_exercise("Por favor resuelve este sistema por Gauss 2x + y = 5; x - y = 1")
        self.assertEqual(parsed.variables, ["x", "y"])
        self.assertEqual(parsed.A, [[2, 1], [1, -1]])
        self.assertEqual(parsed.B, [5, 1])
        self.assertEqual(TechChipAgent().analyze(parsed.A, parsed.B).solution, [2, 1])

    def test_fractions_constants_on_both_sides_and_subscripts(self):
        parsed = parse_exercise("Ecuación 1: 1/2 x₁ + x₂ + 3 = 7\nEcuación 2: x₁ - x₂ = 2")
        self.assertEqual(parsed.variables, ["x1", "x2"])
        self.assertEqual(parsed.A, [[Fraction(1, 2), 1], [1, -1]])
        self.assertEqual(parsed.B, [4, 2])

        scientific = parse_exercise("1e-2x + y = 1; x - y = 0")
        self.assertEqual(scientific.A[0][0], Fraction(1, 100))

    def test_json_and_matrix_notation_inside_prompt(self):
        json_prompt = 'Calcula esto: {"A":[[2,1],[1,-1]],"B":[5,1]}'
        self.assertEqual(parse_exercise(json_prompt).source, "json")
        notation = "Usa Gauss-Jordan con A=[[2,1],[1,-1]] y B=[5,1]"
        parsed = parse_exercise(notation)
        self.assertEqual(parsed.source, "matrix_notation")
        self.assertEqual(parsed.B, [5, 1])

    def test_api_returns_input_analysis_and_variable_mapping(self):
        result = solve_exercise_payload({"exercise": "2x+y=5; x-y=1", "production": False})
        self.assertEqual(result["input"]["A"], [["2", "1"], ["1", "-1"]])
        self.assertEqual(result["analysis"]["solution"], ["2", "1"])
        self.assertEqual(result["variables"], ["x", "y"])

    def test_six_by_six_prompt(self):
        prompt = "; ".join(f"x{i} = {i}" for i in range(1, 7))
        result = solve_exercise_payload({"exercise": prompt})
        self.assertEqual(result["analysis"]["solution"], ["1", "2", "3", "4", "5", "6"])
        self.assertEqual(result["variables"], ["x1", "x2", "x3", "x4", "x5", "x6"])

    def test_ten_by_ten_prompt_and_requested_method(self):
        prompt = "; ".join(f"x{i} = {i}" for i in range(1, 11)) + "; resuelve por Gauss-Jordan"
        parsed = parse_exercise(prompt)
        self.assertEqual(len(parsed.A), 10)
        self.assertEqual(parsed.B, list(range(1, 11)))
        self.assertEqual(parsed.preferred_method, "gauss_jordan")

    def test_flexible_json_keys_and_nested_payload(self):
        parsed = parse_exercise('{"sistema":{"coeficientes":[[2,1],[1,-1]],"disponibilidades":[5,1]}}')
        self.assertEqual(parsed.A, [[2, 1], [1, -1]])
        self.assertEqual(parsed.B, [5, 1])
        augmented = parse_exercise('{"matriz_aumentada":[[2,1,5],[1,-1,1]]}')
        self.assertEqual(augmented.A, [[2, 1], [1, -1]])
        self.assertEqual(augmented.B, [5, 1])

    @patch("exercise_interpreter.urlopen")
    def test_recognized_but_invalid_json_is_not_sent_to_model(self, urlopen):
        with self.assertRaisesRegex(InputError, "A debe tener"):
            interpret_exercise('{"coeficientes":[[1,2]],"disponibilidades":[3]}')
        urlopen.assert_not_called()

    @patch("exercise_interpreter.urlopen")
    def test_natural_language_uses_structured_model_extraction(self, urlopen):
        response = MagicMock()
        response.read.return_value = json.dumps({
            "status": "completed",
            "output_text": json.dumps({
                "status": "ok", "A": [["7", "3"], ["4", "5"]], "B": ["579", "643"],
                "variables": ["producto A", "producto B"], "preferred_method": "gauss_jordan", "clarification": "",
            }),
        }).encode()
        urlopen.return_value.__enter__.return_value = response
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            parsed = interpret_exercise("Dos productos consumen recursos; resuelve por Gauss-Jordan con los datos indicados.")
        self.assertEqual(parsed.source, "llm")
        self.assertEqual(parsed.A, [[7, 3], [4, 5]])
        self.assertEqual(parsed.B, [579, 643])
        self.assertEqual(parsed.preferred_method, "gauss_jordan")
        request_body = json.loads(urlopen.call_args.args[0].data.decode())
        self.assertEqual(request_body["text"]["format"]["type"], "json_schema")
        self.assertFalse(request_body["store"])
        self.assertIn("NOMBRE del recurso", request_body["instructions"])
        self.assertIn("número por número", request_body["instructions"])
        self.assertIn("NUNCA copies ese orden", request_body["instructions"])
        self.assertIn("Acepta redacción libre", request_body["instructions"])
        self.assertIn("no por diferencias de redacción", request_body["instructions"])

    @patch("exercise_interpreter.urlopen")
    def test_natural_language_accepts_public_lowercase_a_b_contract(self, urlopen):
        response = MagicMock()
        response.read.return_value = json.dumps({
            "status": "completed",
            "output_text": json.dumps({
                "status": "ok", "a": [["7", "4"], ["3", "5"]], "b": ["579", "643"],
                "variables": ["P1", "P2"], "preferred_method": "none", "clarification": "",
            }),
        }).encode()
        urlopen.return_value.__enter__.return_value = response
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            parsed = interpret_exercise("7 kg de A y 4 kg de B; disponibilidades 579 y 643")
        self.assertEqual(parsed.A, [[7, 4], [3, 5]])
        self.assertEqual(parsed.B, [579, 643])

    @patch("exercise_interpreter.urlopen")
    def test_ambiguous_model_extraction_requests_clarification(self, urlopen):
        response = MagicMock()
        response.read.return_value = json.dumps({
            "status": "completed",
            "output_text": json.dumps({
                "status": "clarification", "A": [], "B": [], "variables": [],
                "preferred_method": "none", "clarification": "¿Cuánto recurso B consume el segundo producto?",
            }),
        }).encode()
        urlopen.return_value.__enter__.return_value = response
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}), self.assertRaisesRegex(InputError, "Necesito una aclaración"):
            interpret_exercise("El primer producto usa 7 kg; hay 579 kg disponibles.")

    def test_rejects_nonlinear_incomplete_and_unsafe_expressions(self):
        invalid = [
            "x*y = 2; x+y=3",
            "x^2 + y = 3; x-y=1",
            "x+y=2",
            "x1+x3=2; x1-x3=0",
            "__import__('os') = x; x = 1",
            "hola, resuelve una matriz",
        ]
        for prompt in invalid:
            with self.subTest(prompt=prompt), self.assertRaises(InputError):
                parse_exercise(prompt)


if __name__ == "__main__":
    unittest.main()
