import streamlit
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage


def load_prompt(content):
    """Crea un modello di prompt per una lezione interattiva.

        Parameters:
            content (str): Il contenuto della lezione da includere nel prompt.

        Returns:
            langchain.templates.ChatPromptTemplate: Il modello di prompt creato per la lezione.

        Notes:
            La funzione crea un modello di prompt per guidare una lezione interattiva di ingegneria del software.
            Include istruzioni per l'educatore su come guidare l'utente attraverso la lezione.
    """
    
    template = template = (""""I want you to act as a university software engineering professor delivering engaging 
    and concise lectures to Italian students. Your expertise lies in explaining SWEBOK chapters in English to your 
    students in Italian.You are an expert educator and are responsible for guiding the user through this lesson plan. 
    Ensure you help them progress appropriately and encourage them along the way. If they ask off-topic questions, 
    politely decline and remind them to stay on topic. Please limit responses to one concept or step at a time. Each 
    step should contain no more than ~5 lines. Ensure they fully understand before proceeding. This is an interactive 
    lesson - engage and guide them, don't lecture. ----------------- {content} ----------------- End of Content.

    End of Lesson."""
                           .format(content=content))

    prompt_template = ChatPromptTemplate(messages=[
        SystemMessage(content=template),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    return prompt_template


def load_prompt_with_questions(content):
    """Crea un modello di prompt interattivo con domande per una lezione.

        Parameters:
            content (str): Il contenuto della lezione da includere nel prompt.

        Returns:
            langchain.templates.ChatPromptTemplate: Il modello di prompt creato per la lezione con domande.

        Notes:
            La funzione crea un modello di prompt per una lezione interattiva in cui vengono fornite delle domande
            all'utente dopo ogni breve lezione. Si aspetta risposte corrette dall'utente prima di procedere.
    """
    
    template = """"I want you to act as a university software engineering professor delivering engaging and concise 
    lectures to Italian students. Your expertise lies in explaining SWEBOK chapters in English to your students in 
    Italian.You are an expert educator, and are responsible for walking the user through this lesson plan. You should 
    make sure to guide them along, encouraging them to progress when appropriate. If they ask questions not related 
    to this getting started guide, you should politely decline to answer and remind them to stay on topic. You should 
    ask them questions about the instructions after each instructions and verify their response is correct before 
    proceeding to make sure they understand the lesson. Whenever the user answers correctly to your questions, 
    write these exact words: -Hai risposto correttamente. If they make a mistake, give them good explanations and 
    encourage them to answer your questions, instead of just moving forward to the next step.

    Please limit any responses to only one concept or step at a time.
    Each step show only be ~15 lines at MOST.
    Make sure they fully understand that before moving on to the next. 
    This is an interactive lesson - do not lecture them, but rather engage and guide them along!
    -----------------

    {content}

    -----------------
    End of Content.

    Now remember short response with only 1 code snippet per message and ask questions to test user knowledge right 
    after every short lesson. Only one question per message. Only one lesson per message.

    Your teaching should be in the following interactive format:

    Short lesson 3-5 sentences long
    Questions about the short lesson (1-3 questions)

    Short lesson 3-5 sentences long
    Questions about the short lesson (1-3 questions)
    ...

    """.format(content=content)

    prompt_template = ChatPromptTemplate(messages=[
        SystemMessage(content=template),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    return prompt_template


def get_lesson_guide(connection):
    """Ottiene la guida delle lezioni per l'utente loggato dal database.

        Parameters:
            connection (mysql.connector.connection.MySQLConnection): La connessione al database MySQL.

        Returns:
            dict: Un dizionario contenente le informazioni delle lezioni per l'utente.

        Notes:
            La funzione esegue una query per ottenere le informazioni delle lezioni disponibili per l'utente loggato.
            Le informazioni includono l'ID della lezione, il nome, la descrizione e il percorso del file.
    """
    
    cursor = connection.cursor()

    lesson_guides = {}
    query = "SELECT id, nome, descrizione, percorso_file FROM Lezioni where username= %s "
    values = (streamlit.session_state.username,)

    try:
        cursor.execute(query, values)

        # Estrai i risultati
        results = cursor.fetchall()

        # Itera attraverso i risultati e aggiungi le informazioni a lesson_guides
        for result in results:
            id_lezione, nome_lezione, descrizione, percorso_file = result
            lesson_guides[nome_lezione] = {
                "id": id_lezione,
                "description": descrizione,
                "file": percorso_file

            }
    except Exception as e:
        print(f"Errore durante l'esecuzione della query: {e}")

    return lesson_guides
