import streamlit as st
import streamlit_authenticator as stauth
import secrets
import re

# Credenziali
credentials = {'usernames': {'user1': 'pass123'}}

# Genera chiave random
key = secrets.token_urlsafe(16)

# Inizializza login manager
login_manager = stauth.Authenticate(credentials,
                                    cookie_name='auth',
                                    key=key)

# Variabile globale password validata
validated_password = ""


def validate_password(password):
    global validated_password

    # Controllo lunghezza
    if len(password) < 8:
        st.error("Password troppo corta")
        return

    # Controllo maiuscolo
    if not any(char.isupper() for char in password):
        st.error("Inserisci almeno 1 maiuscola")
        return

        # Controllo carattere speciale
    if not re.search(r'[!@#$]', password):
        st.error("Inserisci almeno 1 carattere speciale")
        return

    validated_password = password
    return validated_password


def app():
    choice = st.sidebar.selectbox("Choice", ["Login", "Register"])

    if choice == "Login":

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_manager.login(username, password):
                st.success("Login effettuato")
            else:
                st.error("Credenziali non valide")

    elif choice == "Register":

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if validate_password(password):

            confirm_password = st.text_input("Confirm Password")

            if st.button("Register") and validated_password == confirm_password:
                credentials['usernames'][username] = validated_password
                st.success("Registrato!")


if __name__ == '__main__':
    app()

