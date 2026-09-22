"""Ejercicios escritos: conversión exacta y rechazo de expresiones inseguras."""
from fractions import Fraction
import unittest

from agent import InputError, TechChipAgent
from api.solve import solve_exercise_payload
from exercise_parser import parse_exercise


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
