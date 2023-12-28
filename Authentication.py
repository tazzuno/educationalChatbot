import streamlit as st
import streamlit_authenticator as stauth
import secrets
import bcrypt
import re
import mysql.connector
import openai
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
  """Connette al database MySQL utilizzando le informazioni di connessione fornite nei secrets di Streamlit.

        Returns:
        mysql.connector.connection.MySQLConnection or None: Una connessione al database MySQL se la connessione è
        riuscita con successo, altrimenti None.
  """
    try:
        # Recupera le informazioni di connessione dal file secrets
        return mysql.connector.connect(**st.secrets["mysql"])
    except Exception as e:
        st.error(f"Errore di connessione al database: {e}")
        return None


def chiudi_connessione_database(connection):
  """Chiude la connessione al database MySQL se è attiva e aperta.

        Parameters:
            connection (mysql.connector.connection.MySQLConnection): La connessione al database MySQL da chiudere.

        Notes:
            La funzione controlla se la connessione è attiva e aperta prima di chiuderla.
  """
    if connection and connection.is_connected():
        connection.close()


def validate_password(password):
  """Valida una password secondo determinati criteri.

        Parameters:
            password (str): La password da validare.

        Returns:
            str or None: La password validata se rispetta i criteri, altrimenti None.

        Notes:
            La funzione verifica se la password soddisfa i seguenti criteri:
            - Deve essere lunga almeno 8 caratteri.
            - Deve contenere almeno una lettera maiuscola.
            - Deve contenere almeno un carattere speciale tra !, @, # o $.
  """
    global validated_password

    if len(password) > 0:

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


def is_api_key_valid(key):
  """Verifica la validità di una chiave API di OpenAI eseguendo una richiesta di completamento.

        Parameters:
            key (str): La chiave API da verificare.

        Returns:
            bool or str: True se la chiave API è valida, altrimenti False o una stringa che rappresenta l'errore.

        Notes:
            La funzione imposta la chiave API fornita e tenta di eseguire una richiesta di completamento
            utilizzando OpenAI's Completion API con un'istanza di motore "davinci".
  """
    try:
        openai.api_key = key
        response = openai.Completion.create(
            engine="davinci",  # https://platform.openai.com/docs/models
            prompt="This is a test.",
            max_tokens=5
        )
    except Exception as ex:
        return str(ex)
        return False
    else:
        return True


def aggiungi_utente_al_database(username, password, email, api_key, connection):
  """Aggiunge un nuovo utente al database.

        Parameters:
            username (str): Il nome utente dell'utente da aggiungere.
            password (str): La password dell'utente da aggiungere.
            email (str): L'email dell'utente da aggiungere.
            api_key (str): La chiave API dell'utente da aggiungere.
            connection (mysql.connector.connection.MySQLConnection): La connessione al database MySQL.

        Notes:
            La funzione esegue l'hash della password fornita prima di salvarla nel database.
  """
    if connection:
        try:
            cursor = connection.cursor()

            # Aggiungi l'utente al database
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            cursor = connection.cursor()
            query = '''INSERT INTO Utenti (Username, Password, Email, API_key) VALUES (%s, %s, %s, %s)'''
            args = (username, password, email, api_key)
            cursor.execute(query, args)
            connection.commit()

        except Error as e:
            print(f"Errore durante l'aggiunta dell'utente al database: {e}")
        finally:
            chiudi_connessione_database(connection)


def verifica_credenziali(username, password, connection):
  """Verifica le credenziali di accesso di un utente nel database.

        Parameters:
            username (str): Il nome utente dell'utente da verificare.
            password (str): La password dell'utente da verificare.
            connection (mysql.connector.connection.MySQLConnection): La connessione al database MySQL.

        Returns:
            int: 1 se le credenziali sono valide, altrimenti 0.

        Notes:
            La funzione esegue una query per controllare se le credenziali fornite corrispondono a un utente nel database.
  """
    if connection:
        try:
            cursor = connection.cursor()

            query = "SELECT * FROM utenti WHERE username = %s AND password = %s"
            values = (username, password)

            cursor.execute(query, values)

            # Estrai i risultati
            result = cursor.fetchall()

            # Mostra il risultato
            if result:
                return 1
            else:
                return 0

        except Error as e:
            print(f"Errore durante l'aggiunta dell'utente al database: {e}")
        finally:
            chiudi_connessione_database(connection)



