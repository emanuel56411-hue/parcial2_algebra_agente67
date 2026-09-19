import streamlit as st
import numpy as np
import pandas as pd
from agent import TechChipAgent

# Configuración de página
st.set_page_config(page_title="TechChip Systems - Agente IA", page_icon="🤖", layout="wide")

st.title(" Agente IA - Balanceo de Planta TechChip Systems")
st.markdown("Optimización matricial $6 \\times 6$ e interpretación de operaciones en tiempo real.")

agent = TechChipAgent()

# Matriz A base
A_base = np.array([
    [2, 1, 3, 1, 2, 1],
    [1, 3, 2, 2, 1, 2],
    [3, 2, 4, 1, 3, 2],
    [1, 1, 1, 4, 2, 1],
    [2, 1, 2, 1, 5, 3],
    [1, 2, 1, 2, 1, 4]
], dtype=float)

# Sidebar: Selector de Escenarios de Prueba
st.sidebar.header(" Batería de Escenarios")
option = st.sidebar.selectbox(
    "Selecciona un escenario para probar:",
    ("Prueba 1: Escenario Base", "Prueba 3: Escasez de Resina (B3 = 100)", "Prueba 4: Matriz Degenerada (det = 0)", "Personalizado")
)

# Configurar Vector B y Matriz A según selección
X_target = np.array([15, 20, 25, 10, 15, 20])
B_current = np.dot(A_base, X_target)
A_current = A_base.copy()

if option == "Prueba 3: Escasez de Resina (B3 = 100)":
    B_current[2] = 100.0
elif option == "Prueba 4: Matriz Degenerada (det = 0)":
    A_current[5, :] = 2.0 * A_current[0, :]

# Visualización de datos de entrada
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Matriz A (Coeficientes de Consumo)")
    df_A = pd.DataFrame(A_current, columns=agent.products)
    st.dataframe(df_A, use_container_width=True)

with col2:
    st.subheader("Vector B (Disponibilidad)")
    df_B = pd.DataFrame(B_current, columns=["Capacidad Total"])
    st.dataframe(df_B, use_container_width=True)

# Botón de resolución
if st.button(" Ejecutar Análisis con el Agente IA"):
    x_sol, diag, msg = agent.analyze_and_solve(A_current, B_current)
    
    st.divider()
    st.subheader("Diagnóstico del Sistema")
    
    # Metricas principales
    m1, m2, m3 = st.columns(3)
    m1.metric("Determinante det(A)", f"{diag['det']:.2f}")
    m2.metric("Rango Matriz A", diag['rank_A'])
    m3.metric("Rango Ampliado [A|B]", diag['rank_aug'])

    if diag["is_singular"]:
        st.error(msg)
    else:
        st.success(msg)
        
        # Error residual
        error = np.linalg.norm(np.dot(A_current, x_sol) - B_current)
        st.info(f"Error Absoluto ||AX - B||: `{error:.2e}`")
        
        
        # Tabla de resultados
        st.subheader(" Plan de Producción Calculado")
        res_data = []
        has_negative = False
        for prod, val in zip(agent.products, x_sol):
            units = int(round(val * 1000))
            is_neg = val < -1e-6
            if is_neg:
                has_negative = True
            res_data.append({
                "Línea de Módulo": prod,
                "Producción (k Unidades)": f"{val:.2f}",
                "Unidades Totales": f"{units:,}",
                "Estado": " INVIABLE (Déficit)" if is_neg else " ÓPTIMO"
            })
            
        st.table(pd.DataFrame(res_data))
        
        if has_negative:
            st.warning(" **Diagnóstico de Negocio:** Plan inalcanzable por restricción de materias primas.")
        else:
            st.balloons()
            st.success(" **Diagnóstico de Negocio:** Asignación balanceada al 100% de capacidad sin cuellos de botella.")