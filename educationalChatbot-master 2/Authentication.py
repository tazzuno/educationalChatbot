import streamlit as st
import streamlit_authenticator as stauth
import secrets
import bcrypt
import re
import mysql.connector
from mysql.connector import Error

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


def connetti_database():
    try:
        # Recupera le informazioni di connessione dal file secrets
        return mysql.connector.connect(**st.secrets["mysql"])
    except Exception as e:
        st.error(f"Errore di connessione al database: {e}")
        return None


def chiudi_connessione_database(connection):
    if connection and connection.is_connected():
        connection.close()


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


def aggiungi_utente_al_database(username, password, email, api_key, connection):
    if connection:
        try:
            cursor = connection.cursor()

            # Aggiungi l'utente al database
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            query = "INSERT INTO Utenti (Username, Password, Email, API_key) VALUES (%s, %s, %s, %s)"
            data = (username, hashed_password, email, api_key)
            cursor.execute(query, data)
            connection.commit()
            print("Utente aggiunto con successo!")

        except Error as e:
            print(f"Errore durante l'aggiunta dell'utente al database: {e}")
        finally:
            chiudi_connessione_database(connection)


def app():
    connection = connetti_database()
    choice = st.sidebar.selectbox("Choice", ["Login", "Register"])

    if choice == "Login":

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_manager.authenticate(username, password):
                st.success("Login effettuato")
            else:
                st.error("Credenziali non valide")

    elif choice == "Register":

        email = st.text_input("Email")
        username = st.text_input("Username")
        api_key = st.text_input("API KEY (CHAT-GPT)")
        password = st.text_input("Password", type="password")

        if validate_password(password):
            confirm_password = st.text_input("Confirm Password")

            if st.button("Register") and validated_password == confirm_password:
                aggiungi_utente_al_database(username, password, email, api_key, connection)
                st.success("Utente registrato!")


if __name__ == '__main__':
    app()
