"""Datos originales de la guía y variantes identificadas explícitamente."""
from copy import deepcopy

A_BASE = [
    [2, 1, 3, 1, 2, 1], [1, 3, 2, 2, 1, 2], [3, 2, 4, 1, 3, 2],
    [1, 1, 1, 4, 2, 1], [2, 1, 2, 1, 5, 3], [1, 2, 1, 2, 1, 4],
]
B_GUIDE = [155, 160, 225, 140, 215, 175]
X_TARGET = [15, 20, 25, 10, 15, 20]
B_TARGET = [185, 200, 280, 150, 245, 195]
PRODUCTS = ["AI-Edge 1", "AI-Server Pro", "AI-Autonomous Car", "AI-IoT LowPower", "AI-Robotics Heavy", "AI-Medical Vision"]
RESOURCES = ["Litografía EUV", "Pruebas ATE", "Resina de encapsulado", "Sustrato de silicio", "Energía láser", "Inspección óptica"]
UNITS = ["horas-máquina", "horas-máquina", "kg", "m²", "MWh", "horas-persona"]
GUIDE_NOTE = (
    "La guía contiene una inconsistencia: el vector esperado (15, 20, 25, 10, 15, 20) "
    "requiere B = (185, 200, 280, 150, 245, 195). No resuelve el B original "
    "(155, 160, 225, 140, 215, 175). Ambos casos se conservan por separado."
)
SCENARIOS = {
    "original": ("TechChip · datos originales", "Disponibilidades transcritas de la guía, sin correcciones ocultas."),
    "compatible": ("TechChip · vector esperado", "Variante didáctica con B = A·X esperado. Esta disponibilidad no es la de la guía."),
    "scarcity": ("Escasez · resina a 100 kg", "Parte de B original y modifica únicamente B₃ = 100."),
    "singular": ("Singular · sin solución", "F₆ = 2F₁, conservando B₆ = 175. La fila 1 exigiría B₆ = 310."),
    "infinite": ("Singular · infinitas soluciones", "F₆ = 2F₁ y B₆ = 2B₁ = 310. Se conserva la dependencia en ambos lados."),
    "example": ("Ejemplo guiado · 3 × 3", "Sistema pequeño con solución X = (2, 3, −1), útil para aprender el procedimiento."),
}


def get_scenario(key: str) -> tuple[list, list]:
    if key not in SCENARIOS:
        raise ValueError(f"Escenario desconocido: {key}")
    A, B = deepcopy(A_BASE), B_GUIDE[:]
    if key == "compatible":
        B = B_TARGET[:]
    elif key == "scarcity":
        B[2] = 100
    elif key in ("singular", "infinite"):
        A[5] = [2 * v for v in A[0]]
        if key == "infinite":
            B[5] = 2 * B[0]
    elif key == "example":
        A, B = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3]
    return A, B
