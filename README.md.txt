# Documentazione del Progetto AIDE

Questo documento fornisce una panoramica generale del progetto AIDE.

## Struttura delle Cartelle

- **images:** Contiene le immagini dei loghi della piattaforma.
- **lessons:** Contiene le lezioni in formato TXT formattate in markdown.
- **aide.sql:** Il database esportato.
- **authentication.py:** Modulo relativo all'autenticazione.
- **get_prompt.py:** Modulo relativo alla gestione e al caricamento dei prompt insieme al contenuto delle lezioni.
- **Lezioni.py:** Modulo che gestisce la schermata principale della piattaforma (chatbot, menu, widget).
- **main.py:** Mette in comunicazione autenticazione e lezioni ed è il file da eseguire per far funzionare l'applicazione.
- **streamHandler.py:** Rappresenta una classe richiamata nella funzione `run_langchain_model` di Lezioni.py per mostrare in tempo reale i token generati dal LLM.

## Come Far Funzionare l'Applicazione

Per far funzionare correttamente l'applicazione, seguire i passaggi seguenti:

1. **Importazione del Progetto in un IDE:**
   - Scaricare il progetto dalla repository.
   - Importare il progetto in un ambiente di sviluppo integrato (IDE) come Visual Studio Code o PyCharm.

2. **Impostazione del Server MySQL Locale:**
   - Installare un server MySQL locale, ad esempio utilizzando XAMPP.
   - Avviare il server MySQL e assicurarsi che sia in esecuzione.

3. **Creazione del Database:**
   - Accedere alla pagina di PHPMyAdmin del server locale (solitamente all'indirizzo http://localhost/phpmyadmin/).
   - Creare un nuovo database chiamato `aide`.

4. **Importazione del Database:**
   - Selezionare il database appena creato (`aide`).
   - Nella scheda "Importa", scegliere il file `aide.sql` dalla directory del progetto.
   - Fare clic su "Esegui" per importare le tabelle nel database.

5. **Esecuzione dell'App:**
   - Aprire il terminale dell'IDE.
   - Posizionarsi nella directory del progetto.
   - Digitare il seguente comando per avviare l'app:
     ```bash
     streamlit run main.py
     ```
   - Premere `Enter` per eseguire l'applicazione.

6. **Accesso all'App:**
   - Dopo aver eseguito l'app, accedere a un browser e visitare l'indirizzo fornito dal terminale (solitamente http://localhost:8501).
   - L'app sarà ora accessibile e funzionante.

7. **Gestione degli Utenti:**
   - Le informazioni relative agli utenti registrati nel database sono già presenti nel file `aide.sql`.
   - È possibile utilizzare gli account esistenti per l'accesso o aggiungere nuovi utenti se il server locale è stato configurato.

Ora l'applicazione è pronta per essere utilizzata! In caso di problemi o domande, fare riferimento alla documentazione o contattare gli sviluppatori.