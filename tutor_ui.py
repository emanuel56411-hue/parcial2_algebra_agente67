"""Controles Streamlit del tutor opcional; las claves nunca llegan al navegador."""
import os
from pathlib import Path
import tomllib

import streamlit as st

from ai_tutor import DEFAULT_MODEL, MAX_QUESTION_CHARS, TutorError, TutorSettings, ask_tutor, build_context

ROOT = Path(__file__).resolve().parent


def settings():
    def value(name, default=""):
        if os.environ.get(name):
            return os.environ[name]
        try:
            return st.secrets.get(name, default)
        except FileNotFoundError:
            return default
    try:
        return TutorSettings(str(value("OPENAI_API_KEY")).strip(), str(value("OPENAI_MODEL", DEFAULT_MODEL)).strip(), int(value("OPENAI_DAILY_REQUEST_LIMIT", 50)))
    except (FileNotFoundError, tomllib.TOMLDecodeError, ValueError):
        return TutorSettings("")


def reset_conversation():
    for key in ("tutor_messages", "tutor_step_answers", "tutor_error"):
        st.session_state.pop(key, None)


def request_answer(config, report, title, note, question, history, method=None, step_index=0):
    context = build_context(report, title, note, method, step_index)
    with st.spinner("Preparando una explicación del cálculo…"):
        answer = ask_tutor(config, context, question, history, ROOT / ".tutor/usage.sqlite3", report, method, step_index if method else None)
    used = st.session_state.get("tutor_tokens", 0)
    st.session_state.tutor_tokens = used + answer.input_tokens + answer.output_tokens
    return answer


def show_answer(answer):
    st.write(answer.text)
    if answer.source == "engine":
        st.caption("Explicación generada por el motor")
    if answer.incomplete:
        st.caption("La respuesta alcanzó el límite de longitud y puede estar incompleta.")
    st.caption(f"Uso de esta respuesta: {answer.input_tokens} tokens de entrada · {answer.output_tokens} de salida.")


def render_step_tutor(report, title, note, method, step_index):
    with st.expander("Ayuda de IA para este paso"):
        config = settings()
        st.caption("Al pulsar el botón se envían a OpenAI los datos del sistema y las matrices de este paso. La consulta consume saldo de la API.")
        if not config.api_key:
            st.info("El tutor está pendiente de activación por el administrador. Puedes consultar la explicación matemática que aparece arriba.")
        key = (method, step_index)
        answers = st.session_state.setdefault("tutor_step_answers", {})
        if st.button("Explicar este paso con IA", key="tutor_explain_step", disabled=not config.api_key, icon=":material/auto_awesome:"):
            try:
                answers[key] = request_answer(config, report, title, note, "Explica este paso: qué operación se aplicó, por qué conserva las soluciones y cómo se comprueba con la matriz anterior.", [], method, step_index)
            except TutorError as exc:
                st.error(str(exc))
        if key in answers:
            show_answer(answers[key])


def render_tutor(report, title, note):
    st.subheader("Pregunta sobre tu resultado")
    st.caption("Al enviar una pregunta, compartes con OpenAI los datos del sistema, el resultado y los últimos mensajes del chat. El tutor puede equivocarse; contrasta sus explicaciones con los pasos exactos.")
    config = settings()
    if not config.api_key:
        st.info("El tutor está pendiente de activación por el administrador. La calculadora y sus procedimientos ya funcionan.")
    else:
        st.caption(f"Modelo: {config.model} · Hasta {config.daily_limit} consultas por día en este servidor · Cada consulta consume saldo de la API.")
    messages = st.session_state.setdefault("tutor_messages", [])
    if st.button("Borrar conversación", key="tutor_clear_chat", disabled=not messages):
        messages.clear()
        st.session_state.pop("tutor_error", None)
    if not messages:
        st.markdown("Puedes preguntar: **¿Por qué aparece un valor negativo?**, **¿qué significan los rangos?** o **¿cómo redacto una conclusión?**")
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if question := st.chat_input("Pregunta sobre el sistema resuelto", key="tutor_prompt", max_chars=MAX_QUESTION_CHARS, disabled=not config.api_key, submit_mode="disable"):
        try:
            answer = request_answer(config, report, title, note, question, messages)
        except TutorError as exc:
            st.session_state.tutor_error = str(exc)
        else:
            st.session_state.pop("tutor_error", None)
            messages.extend([{"role": "user", "content": question}, {"role": "assistant", "content": answer.text}])
            del messages[:-12]
            with st.chat_message("user"):
                st.markdown(question)
            with st.chat_message("assistant"):
                show_answer(answer)
    if st.session_state.get("tutor_error"):
        st.error(st.session_state.tutor_error)
    if st.session_state.get("tutor_tokens"):
        st.caption(f"Tokens registrados en esta sesión, entre chat y explicación de pasos: {st.session_state.tutor_tokens}.")
