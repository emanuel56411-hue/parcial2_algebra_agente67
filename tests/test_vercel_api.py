import unittest

from agent import InputError
from api.solve import solve_payload


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


if __name__ == "__main__":
    unittest.main()
