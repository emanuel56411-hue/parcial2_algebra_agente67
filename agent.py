import numpy as np
from rich.console import Console
from rich.table import Table

console = Console()

class LinearAlgebraSolver:
    @staticmethod
    def validate(A, B):
        A = np.array(A, dtype=float)
        B = np.array(B, dtype=float).reshape(-1, 1)
        det = np.linalg.det(A)
        rank_A = np.linalg.matrix_rank(A)
        aug = np.hstack((A, B))
        rank_aug = np.linalg.matrix_rank(aug)
        return {
            "det": det,
            "rank_A": rank_A,
            "rank_aug": rank_aug,
            "is_singular": abs(det) < 1e-9,
            "is_compatible": rank_A == rank_aug
        }

    @staticmethod
    def solve_gauss(A, B):
        M = np.hstack((np.array(A, dtype=float), np.array(B, dtype=float).reshape(-1, 1)))
        n = len(M)
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(M[r, i]))
            if i != max_row:
                M[[i, max_row]] = M[[max_row, i]]
            pivot = M[i, i]
            if abs(pivot) < 1e-9:
                raise ValueError("Pivote nulo.")
            for j in range(i + 1, n):
                factor = M[j, i] / pivot
                M[j, i:] -= factor * M[i, i:]
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            sum_ax = np.dot(M[i, i+1:n], x[i+1:n])
            x[i] = (M[i, -1] - sum_ax) / M[i, i]
        return x

class TechChipAgent:
    def __init__(self):
        self.products = [
            "AI-Edge 1", "AI-Server Pro", "AI-Autonomous Car", 
            "AI-IoT LowPower", "AI-Robotics Heavy", "AI-Medical Vision"
        ]
        self.solver = LinearAlgebraSolver()

    def analyze_and_solve(self, A, B):
        diag = self.solver.validate(A, B)
        if diag["is_singular"]:
            if not diag["is_compatible"]:
                return None, diag, "[ERROR] SISTEMA INCOMPATIBLE: Sin solucion."
            return None, diag, "[ADVERTENCIA] SISTEMA COMPATIBLE INDETERMINADO: Infinitas soluciones."
        
        x = self.solver.solve_gauss(A, B)
        return x, diag, "[OK] SISTEMA COMPATIBLE DETERMINADO: Solucion unica."

    def print_report(self, x, error, title="Reporte Operacional"):
        table = Table(title=f"REPORTE: {title}")
        table.add_column("Linea de Modulo", style="cyan")
        table.add_column("Produccion (k Unidades)", style="magenta")
        table.add_column("Total Procesadores", style="green")
        table.add_column("Estado", style="bold")

        has_negative = False
        for prod, val in zip(self.products, x):
            units = int(round(val * 1000))
            if val < -1e-6:
                has_negative = True
                status = "[red]INVIABLE[/red]"
            else:
                status = "[green]OPTIMO[/green]"
            table.add_row(prod, f"{val:.2f}", f"{units:,}", status)

        console.print(table)
        console.print(f"Error Absoluto ||AX - B||: [yellow]{error:.2e}[/yellow]\n")
        if has_negative:
            console.print("[ADVERTENCIA] DIAGNOSTICO: Plan inalcanzable por restriccion de insumos.\n")
        else:
            console.print("[OK] DIAGNOSTICO: Produccion balanceada al 100% de capacidad.\n")