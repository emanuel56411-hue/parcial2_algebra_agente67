"""Pruebas de resultados, invariantes y reproducción de las trazas."""
from copy import deepcopy
from fractions import Fraction as F
from itertools import permutations
import json
from pathlib import Path
import random
import subprocess
import sys
import unittest

from agent import InputError, LinearAlgebraSolver, TechChipAgent, matvec, parse_json, validate_input
from main import validation_battery
from reporting import html_report, markdown_report
from scenarios import A_BASE, B_GUIDE, B_TARGET, X_TARGET, get_scenario

ROOT = Path(__file__).resolve().parents[1]


def determinant_definition(A):
    """Oráculo independiente por permutaciones; solo para matrices pequeñas."""
    total = F(0)
    for p in permutations(range(len(A))):
        inversions = sum(p[i] > p[j] for i in range(len(A)) for j in range(i + 1, len(A)))
        term = F((-1) ** inversions)
        for i, j in enumerate(p):
            term *= A[i][j]
        total += term
    return total


class SolverTests(unittest.TestCase):
    def setUp(self):
        self.agent = TechChipAgent()

    def test_original_data_are_not_replaced(self):
        report = self.agent.analyze(A_BASE, B_GUIDE, production=True)
        self.assertEqual(report.determinant, -83)
        self.assertEqual(report.solution, [F(v, 83) for v in [-105, 345, 2430, 1170, 1130, 2010]])
        self.assertNotEqual(matvec(A_BASE, X_TARGET), B_GUIDE)
        self.assertEqual(matvec(A_BASE, X_TARGET), B_TARGET)
        self.assertEqual(report.max_error, 0)
        self.assertIn("inalcanzable", report.interpretation[0])

    def test_expected_vector_is_separate_scenario(self):
        report = self.agent.analyze(*get_scenario("compatible"), production=True)
        self.assertEqual(report.solution, X_TARGET)
        self.assertTrue(report.methods_agree)
        self.assertEqual(report.residual, [0] * 6)
        self.assertIn("factible", report.interpretation[0])

    def test_scarcity(self):
        report = self.agent.analyze(*get_scenario("scarcity"), production=True)
        self.assertEqual(report.B, [155, 160, 100, 140, 215, 175])
        self.assertEqual(report.solution[:2], [F(-26355, 83), F(-6780, 83)])
        self.assertEqual(report.residual, [0] * 6)

    def test_singular_inconsistent(self):
        report = self.agent.analyze(*get_scenario("singular"))
        self.assertEqual((report.status, report.determinant, report.rank_A, report.rank_augmented), ("inconsistent", 0, 5, 6))
        self.assertFalse(report.methods)
        self.assertIsNone(report.solution)
        self.assertTrue(any("Contradicción" in s.operation for s in report.diagnostic_steps))

    def test_infinite_family(self):
        report = self.agent.analyze(*get_scenario("infinite"))
        self.assertEqual((report.status, report.rank_A, report.rank_augmented), ("infinite", 5, 5))
        self.assertEqual(len(report.nullspace), 1)
        self.assertEqual(matvec(report.A, report.particular), report.B)
        for vector in report.nullspace:
            self.assertEqual(matvec(report.A, vector), [0] * 6)
            for t in [F(-17, 3), F(0), F(99)]:
                self.assertEqual(matvec(report.A, [p + t*v for p, v in zip(report.particular, vector)]), report.B)

    def test_zero_matrix_and_free_leading_columns(self):
        for A, B, rank in [([[0, 0], [0, 0]], [0, 0], 0), ([[0, 2], [0, 4]], [6, 12], 1)]:
            with self.subTest(A=A):
                report = self.agent.analyze(A, B)
                self.assertEqual(report.status, "infinite")
                self.assertEqual(report.rank_A, rank)
                self.assertEqual(matvec(report.A, report.particular), report.B)
                self.assertEqual(len(report.nullspace), len(A)-rank)
        self.assertEqual(self.agent.analyze([[0, 0], [0, 0]], [0, 1]).rank_augmented, 1)

    def test_small_nonzero_determinant_is_not_singular(self):
        report = self.agent.analyze([["1e-30", 0], [0, "1e-30"]], ["2e-30", "3e-30"])
        self.assertEqual(report.status, "unique")
        self.assertEqual(report.determinant, F(1, 10**60))
        self.assertEqual(report.solution, [2, 3])

    def test_partial_pivot_and_sign_of_determinant(self):
        report = self.agent.analyze([[0, 1], [2, 3]], [2, 8])
        self.assertEqual(report.solution, [1, 2])
        self.assertEqual(report.determinant, -2)
        self.assertEqual(report.methods["gauss"].steps[1].kind, "swap")

    def test_determinant_matches_definition(self):
        rng = random.Random(37)
        for n in range(1, 5):
            for _ in range(8):
                A = [[F(rng.randint(-4, 4)) for _ in range(n)] for _ in range(n)]
                with self.subTest(A=A):
                    self.assertEqual(self.agent.analyze(A, [0]*n).determinant, determinant_definition(A))

    def test_generated_known_solutions_all_sizes(self):
        rng = random.Random(91)
        for n in [1, 2, 3, 6, 12]:
            A = [[F(rng.randint(-3, 3)) for _ in range(n)] for _ in range(n)]
            for i in range(n):
                A[i][i] = sum(abs(v) for v in A[i]) + 1
            expected = [F(rng.randint(-7, 7), 3) for _ in range(n)]
            report = self.agent.analyze(A, matvec(A, expected))
            with self.subTest(n=n):
                self.assertEqual(report.solution, expected)
                self.assertTrue(report.methods_agree)
                inv = report.methods["inverse"].inverse
                for left, right in [(report.A, inv), (inv, report.A)]:
                    product = [[sum(left[i][k]*right[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
                    self.assertEqual(product, [[int(i==j) for j in range(n)] for i in range(n)])

    def test_replay_every_row_operation(self):
        report = self.agent.analyze(*get_scenario("original"))
        for method in report.methods.values():
            current = deepcopy(method.steps[0].matrix)
            for step in method.steps[1:]:
                if step.kind == "swap":
                    current[step.target], current[step.source] = current[step.source], current[step.target]
                elif step.kind == "scale":
                    current[step.target] = [v*step.factor for v in current[step.target]]
                elif step.kind == "add":
                    current[step.target] = [a+step.factor*b for a,b in zip(current[step.target], current[step.source])]
                self.assertEqual(current, step.matrix, (method.name, step.operation))

    def test_steps_include_structured_presentation_without_removing_legacy_fields(self):
        report = self.agent.analyze([[2, 1], [1, -1]], [5, 1])
        steps = [*report.diagnostic_steps, *(step for method in report.methods.values() for step in method.steps)]
        for step in steps:
            self.assertTrue(step.operation)
            self.assertTrue(step.explanation)
            self.assertTrue(step.title)
            self.assertTrue(step.what)
            self.assertTrue(step.why)
            self.assertLessEqual(len(step.why.split()), 25)
            self.assertIsInstance(step.calc, list)
            self.assertIsInstance(step.changed_rows, list)
            self.assertIsInstance(step.decimals, dict)
        encoded = report.to_dict()
        sample = encoded["methods"]["gauss"]["steps"][-1]
        for field in ("title", "what", "why", "calc", "pivot", "changed_rows", "decimals"):
            self.assertIn(field, sample)
        self.assertTrue(sample["calc"][-1].startswith("Resultado:"))

    def test_inverse_product_has_one_calculation_line_per_term(self):
        report = self.agent.analyze([[2, 1], [1, -1]], [5, 1])
        products = [step for step in report.methods["inverse"].steps if step.kind == "multiplication"]
        self.assertEqual(len(products), 2)
        for step in products:
            self.assertEqual(sum(line.startswith("t") for line in step.calc), 2)
            self.assertTrue(step.calc[-1].startswith("Resultado:"))

    def test_input_is_not_mutated(self):
        A, B = get_scenario("original")
        before = deepcopy((A, B))
        self.agent.analyze(A, B)
        self.assertEqual((A, B), before)

    def test_negative_generic_solution_is_valid(self):
        report = self.agent.analyze([[1]], [-3])
        self.assertEqual(report.solution, [-3])
        self.assertNotIn("inalcanzable", " ".join(report.interpretation))

    def test_production_rejects_negative_resources(self):
        with self.assertRaises(InputError):
            self.agent.analyze([[-1]], [-2], production=True)

    def test_battery(self):
        self.assertTrue(validation_battery()["all_passed"])


class InputTests(unittest.TestCase):
    def test_exact_json_decimals_and_column_B(self):
        A, B = parse_json('{"A": [[0.1, "1/3"], [1, 2]], "B": [[0.3], [1]]}')
        self.assertEqual(A[0], [F(1, 10), F(1, 3)])
        self.assertEqual(B[0], F(3, 10))

    def test_long_valid_decimal_survives_validation_roundtrip(self):
        A, B = parse_json('{"A": [[0.' + '1234567890' * 5 + ']], "B": [1]}')
        report = TechChipAgent().analyze(A, B)
        self.assertEqual(matvec(report.A, report.solution), B)

    def test_reject_invalid_data(self):
        invalid = [([], []), ([[1, 2]], [1]), ([[1], [2]], [1, 2]), ([[1]], []),
                   ([[True]], [1]), ([[None]], [1]), ([["1/0"]], [1]), ([["NaN"]], [1]),
                   ([[float("inf")]], [1]), ([["1e9999999"]], [1]), ([["__import__('os')"]], [1]),
                   ([[1]], [[1, 2]]), ([[1]], [False]), ([[1]*13 for _ in range(13)], [1]*13)]
        for A, B in invalid:
            with self.subTest(A=A), self.assertRaises(InputError):
                validate_input(A, B)

    def test_bad_json(self):
        for text in ["{", "[]", '{"A": [[1]]}', "x"*100_001, '{"A":[[NaN]],"B":[1]}']:
            with self.subTest(text=text[:30]), self.assertRaises(InputError):
                parse_json(text)


class InterfaceTests(unittest.TestCase):
    def test_cli_json_stdin_and_invalid_status(self):
        proc = subprocess.run([sys.executable, "main.py", "--input", "-", "--format", "json"], input='{"A":[[2]],"B":[3]}', text=True, capture_output=True, cwd=ROOT)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["solution"], ["3/2"])
        bad = subprocess.run([sys.executable, "main.py", "--input", "-"], input="{}", text=True, capture_output=True, cwd=ROOT)
        self.assertEqual(bad.returncode, 2)
        self.assertFalse(bad.stdout)
        self.assertIn("Error:", bad.stderr)

    def test_cli_console_input(self):
        proc = subprocess.run([sys.executable, "main.py", "--interactive", "--summary"], input="2\n1 0\n0 1\n4 5\n", text=True, capture_output=True, cwd=ROOT)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("| x2 | 5 |", proc.stdout)

    def test_exports_include_trace_and_escape_html(self):
        report = TechChipAgent().analyze([[2]], [3])
        text = markdown_report(report)
        self.assertIn("Matriz inversa", text)
        self.assertIn("Paso 1", text)
        self.assertIn("3/2", text)
        html = html_report(report, title='<script>alert(1)</script>')
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)
        encoded = json.dumps(report.to_dict(), allow_nan=False)
        self.assertIn("3/2", encoded)


if __name__ == "__main__":
    unittest.main()
