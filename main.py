import numpy as np
from rich.console import Console
from rich.panel import Panel
from agent import TechChipAgent

console = Console()

def run_test_battery():
    agent = TechChipAgent()
    A_base = [
        [2, 1, 3, 1, 2, 1],
        [1, 3, 2, 2, 1, 2],
        [3, 2, 4, 1, 3, 2],
        [1, 1, 1, 4, 2, 1],
        [2, 1, 2, 1, 5, 3],
        [1, 2, 1, 2, 1, 4]
    ]

    console.print(Panel.fit("[bold yellow]BATERIA DE PRUEBAS - AGENTE TECHCHIP SYSTEMS[/bold yellow]"))

    # PRUEBA 1 & 2
    X_target = np.array([15, 20, 25, 10, 15, 20])
    B_base = np.dot(A_base, X_target)
    x_gauss, diag, msg = agent.analyze_and_solve(A_base, B_base)
    error = np.linalg.norm(np.dot(A_base, x_gauss) - B_base)
    agent.print_report(x_gauss, error, title="Prueba 1: Escenario Base")

    # PRUEBA 3
    B_escasez = list(B_base)
    B_escasez[2] = 100.0
    x_esc, _, _ = agent.analyze_and_solve(A_base, B_escasez)
    error_esc = np.linalg.norm(np.dot(A_base, x_esc) - B_escasez)
    agent.print_report(x_esc, error_esc, title="Prueba 3: Escasez B3 = 100")

    # PRUEBA 4
    A_sing = np.array(A_base, dtype=float)
    A_sing[5, :] = 2.0 * A_sing[0, :]
    _, diag_sing, msg_sing = agent.analyze_and_solve(A_sing, B_base)
    console.print(f"[bold red]{msg_sing}[/bold red]\n")

if __name__ == "__main__":
    run_test_battery()