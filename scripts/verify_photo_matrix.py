"""Auditoría independiente de la matriz legible en las fotos del Parcial 2.

El determinante se calcula por la definición de Leibniz y la solución por
Cramer; este archivo no llama a los algoritmos de agent.py.
"""
from fractions import Fraction
from itertools import permutations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scenarios import A_BASE, B_GUIDE, X_TARGET, B_TARGET

PHOTO_A = [
    [2, 1, 3, 1, 2, 1],
    [1, 3, 2, 2, 1, 2],
    [3, 2, 4, 1, 3, 2],
    [1, 1, 1, 4, 2, 1],
    [2, 1, 2, 1, 5, 3],
    [1, 2, 1, 2, 1, 4],
]
PHOTO_B = [155, 160, 225, 140, 215, 175]
PHOTO_EXPECTED_X = [15, 20, 25, 10, 15, 20]


def determinant_by_definition(matrix):
    size = len(matrix)
    total = 0
    for perm in permutations(range(size)):
        inversions = sum(perm[i] > perm[j] for i in range(size) for j in range(i + 1, size))
        product = 1
        for row, column in enumerate(perm):
            product *= matrix[row][column]
        total += (-1 if inversions % 2 else 1) * product
    return total


def cramer_solution(matrix, right):
    det = determinant_by_definition(matrix)
    if det == 0:
        raise ValueError("Cramer requiere determinante distinto de cero")
    return [Fraction(determinant_by_definition([
        [right[row] if column == replaced else matrix[row][column] for column in range(len(matrix))]
        for row in range(len(matrix))
    ]), det) for replaced in range(len(matrix))]


def main():
    assert PHOTO_A == A_BASE, "A del código difiere de la foto"
    assert PHOTO_B == B_GUIDE, "B del código difiere de la foto"
    assert PHOTO_EXPECTED_X == X_TARGET, "X esperado difiere de la foto"
    expected_product = [sum(a * x for a, x in zip(row, PHOTO_EXPECTED_X)) for row in PHOTO_A]
    assert expected_product == B_TARGET
    det = determinant_by_definition(PHOTO_A)
    original = cramer_solution(PHOTO_A, PHOTO_B)
    assert [sum(Fraction(a) * x for a, x in zip(row, original)) for row in PHOTO_A] == list(map(Fraction, PHOTO_B))
    compatible = cramer_solution(PHOTO_A, expected_product)
    assert compatible == list(map(Fraction, PHOTO_EXPECTED_X))
    scarcity_b = PHOTO_B[:]
    scarcity_b[2] = 100
    scarcity = cramer_solution(PHOTO_A, scarcity_b)
    altered_a = [row[:] for row in PHOTO_A]
    altered_a[5] = [2 * value for value in altered_a[0]]
    assert determinant_by_definition(altered_a) == 0
    result = {
        "coincide_codigo_foto": True,
        "determinante_definicion": det,
        "B_foto": PHOTO_B,
        "X_esperado_foto": PHOTO_EXPECTED_X,
        "A_por_X_esperado": expected_product,
        "residuo_vector_esperado": [value - right for value, right in zip(expected_product, PHOTO_B)],
        "error_maximo_vector_esperado": max(abs(value - right) for value, right in zip(expected_product, PHOTO_B)),
        "X_para_B_foto_por_Cramer": [str(value) for value in original],
        "X_para_B_compatible_por_Cramer": [str(value) for value in compatible],
        "X_escasez_por_Cramer": [str(value) for value in scarcity],
        "singular_solo_F6": {"determinante": 0, "B6_impreso": PHOTO_B[5], "B6_exigido": 2 * PHOTO_B[0]},
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
