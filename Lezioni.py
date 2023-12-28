import time
import streamlit as st
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import get_prompt
from langchain.schema import AIMessage, HumanMessage
from StreamHandler import StreamHandler


def handle_messages():
    """Gestisce i messaggi della chat.

    Inizializza lo stato della sessione. Se "messages" non è presente in st.session_state,
    lo inizializza a una lista vuota. Successivamente, gestisce i messaggi presenti in
    st.session_state["messages"], scrivendo i messaggi degli utenti e dell'assistente
    nella chat.

    """
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for msg in st.session_state["messages"]:
        if isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)
        else:
            st.chat_message("assistant").write(msg.content)


def display_lesson(lesson_selection, lesson_info):
    """Visualizza una lezione specifica.

    Parameters:
    lesson_selection (str): Il titolo o la selezione della lezione da visualizzare.
    lesson_info (dict): Un dizionario contenente le informazioni sulla lezione, con la chiave "description" per la descrizione.

    Returns:
    None

    """
    
    with st.container():
        st.markdown(f"**{lesson_selection}**")
        st.write(lesson_info["description"])


def run_langchain_model(prompt, lesson_type, lesson_content, lesson_selection, openai_api_key):
    try:

        # Set up a streaming handler for the model
        with st.chat_message("assistant"):
            stream_handler = StreamHandler(st.empty())
            model = ChatOpenAI(streaming=True, callbacks=[stream_handler], model="gpt-3.5-turbo-16k",
                               openai_api_key=openai_api_key)

            # Load a prompt template based on the lesson type
            if lesson_type == "Instructions based lesson":
                prompt_template = get_prompt.load_prompt(content=lesson_content)
            else:
                prompt_template = get_prompt.load_prompt_with_questions(content=lesson_content)

            # Run a chain of the prompt and the language model
            chain = LLMChain(prompt=prompt_template, llm=model)
            response = chain(
                {"input": prompt, "chat_history": st.session_state.messages[-20:]},
                include_run_info=True,
                tags=[lesson_selection, lesson_type]
            )
            st.session_state.messages.append(HumanMessage(content=prompt))
            st.session_state.messages.append(AIMessage(content=response[chain.output_key]))

    except Exception as e:
        # Handle any errors that occur during the execution of the code
        st.error(f"An error occurred: {e}")


@st.cache_data()
def get_lesson_content(lesson_file):
    try:
        with open(lesson_file, "r") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Error: Lesson file not found at {lesson_file}")
        st.stop()


def download_chat():
    messages = st.session_state.get("messages", [])  # Retrieve messages from session state

    chat_content = "<html><head><link rel='stylesheet' type='text/css' href='styles.css'></head><body>"
    for msg in messages:
        if isinstance(msg, AIMessage):
            chat_content += f"<p class='message ai-message'><strong>AI:</strong> {msg.content}</p>"
        elif isinstance(msg, HumanMessage):
            chat_content += f"<p class='message user-message'><strong>User:</strong> {msg.content}</p>"
        else:
            chat_content += f"<p class='message'>Unknown Message Type: {msg}</p>"

    chat_content += "</body></html>"

    with open("chat.html", "w", encoding="utf-8") as html_file:
        html_file.write(chat_content)

    # Download the generated HTML file
    st.download_button("Download Chat", open("chat.html", "rb"), key="download_chat", file_name="chat.html",
                       mime="text/html")


def save_chat_history(connection, username, lesson_id, chat_history):
    cursor = connection.cursor()
    query = "INSERT INTO chat_history (username, content, sender, lesson_id) VALUES (%s, %s, %s, %s)"
    values = [(username, message.content, message.sender, lesson_id) for message in chat_history]
    cursor.executemany(query, values)
    connection.commit()


def load_chat_history(connection, username, lesson_id):
    cursor = connection.cursor()
    query = "SELECT content, sender FROM chat_history WHERE username = %s AND lesson_id = %s"
    values = (username, lesson_id)
    cursor.execute(query, values)
    result = cursor.fetchall()
    return [HumanMessage(content=row[0]) if row[1] == "user" else AIMessage(content=row[0]) for row in result]


def reset_lesson():
    st.session_state["messages"] = []
    st.session_state["completed_lessons"] = []
    st.session_state["current_lesson"] = None
    st.session_state["current_lesson_type"] = None
    st.session_state["code_snippet"] = None


def setup_page():
    # st.set_page_config(page_title="LangChain: Getting Started Class", page_icon="🦜")
    st.title("AIDE: Getting Started Class with your Study Assinstant")


def avanzamento_barra():
    # inizializzazione variabili
    bar = st.progress(0)
    bar.empty()
    contatore = 0

    messages = st.session_state.get("messages", [])
    for msg in messages:
        if isinstance(msg, AIMessage):
            if msg.content.startswith("Hai risposto correttamente!") or msg.content.startswith("That's correct!"):
                contatore += 1
    progresso = contatore * 10
    bar = st.sidebar.progress(progresso, "Punteggio")
    time.sleep(1)


def load_lesson_content(lesson_file):
    try:
        with open(lesson_file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Error: Lesson file not found at {lesson_file}")
        st.stop()
