from langchain_core.messages import AIMessage

import Authentication as aut
import Lezioni as lz
import streamlit as st


def autenticazione():
    st.title('Autenticazione')
    connection = aut.connetti_database()
    choice = st.sidebar.selectbox("Choice", ["Login", "Register"])

    if choice == "Login":

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if aut.verifica_credenziali(username, password, connection):
                st.success("Login effettuato")
                st.session_state.pagina_corrente = 'Lezioni'
            else:
                st.error("Credenziali non valide")

    elif choice == "Register":

        email = st.text_input("Email")
        username = st.text_input("Username")
        api_key = st.text_input("OPENAI API-KEY", type="password")
        password = st.text_input("Password", type="password")

        if aut.validate_password(password) and aut.is_api_key_valid(api_key):
            confirm_password = st.text_input("Confirm Password")

            if st.button("Register") and aut.validated_password == confirm_password:
                aut.aggiungi_utente_al_database(username, password, email, api_key, connection)
                st.success("Utente registrato!")
            elif aut.validated_password != confirm_password:
                st.error("Le password inserite non coincidono")


def lezioni():
    st.title('Lezioni')
    lz.setup_page()

    lesson_selection = st.sidebar.selectbox("Select Lesson", list(lz.get_prompt.get_lesson_guide().keys()))
    lesson_info = lz.get_prompt.get_lesson_guide()[lesson_selection]
    lesson_content = lz.load_lesson_content(lesson_info["file"])

    lesson_type = st.sidebar.radio("Select Lesson Type",
                                   ["Instructions based lesson", "Interactive lesson with questions"])

    if st.session_state.get("current_lesson") != lesson_selection or st.session_state.get(
            "current_lesson_type") != lesson_type:
        st.session_state["current_lesson"] = lesson_selection
        st.session_state["current_lesson_type"] = lesson_type
        st.session_state["messages"] = [AIMessage(
            content="Benvenuto! Sono AiDe, il tuo assistente virtuale che ti guiderà nell'apprendimento "
                    "dell'ingegneria del software. Scrivimi un messaggio non appena sei pronto per iniziare!"
        )]

    lz.display_lesson(lesson_selection, lesson_info)
    lz.handle_messages()

    if prompt := st.chat_input():
        st.chat_message("user").write(prompt)
        lz.run_langchain_model(prompt, lesson_type, lesson_content, lesson_selection)

    lz.download_chat()
    st.sidebar.button("Reset Lesson", on_click=lz.reset_lesson)
    container_checkbox = st.sidebar.container()
    container_button = st.empty()

    if st.sidebar.checkbox('Show Progress'):
        container_button.empty()
        container_centrale = lz.avanzamento_barra()
    else:
        container_centrale = st.empty()


if 'pagina_corrente' not in st.session_state:
    st.session_state.pagina_corrente = 'Autenticazione'

# Mostra la pagina corrente
if st.session_state.pagina_corrente == 'Autenticazione':
    autenticazione()
elif st.session_state.pagina_corrente == 'Lezioni':
    lezioni()
