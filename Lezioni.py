import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import get_prompt
from langchain.schema import AIMessage, HumanMessage
from StreamHandler import StreamHandler

# Load the OpenAI API key from a .env file
load_dotenv(find_dotenv('secrets.env'))
openai_api_key = os.getenv("SECRET_KEY")


def handle_messages():
    messages = st.session_state.get("messages", [])
    for msg in messages:
        chat_type = "user" if isinstance(msg, HumanMessage) else "assistant"
        st.chat_message(chat_type).write(msg.content)


def run_langchain_model(prompt, lesson_type, lesson_content):
    try:
        # Set up a streaming handler for the model
        with st.chat_message("assistant"):
            stream_handler = StreamHandler(st.empty())
            model = ChatOpenAI(streaming=True, callbacks=[stream_handler], model="gpt-3.5-turbo-16k",
                               openai_api_key=openai_api_key, temperature=0.5, )

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
        # Log the full traceback for debugging
        st.exception(e)


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

    chat_content = (
        "<html><head><link rel='stylesheet' type='text/css' href='styles.css'></head><body>"
        "<div class='chat-container'>"
    )
    for msg in messages:
        if isinstance(msg, AIMessage):
            chat_content += (
                f"<div class='message ai-message'><p><strong>AI:</strong> {msg.content}</p></div>"
            )
        elif isinstance(msg, HumanMessage):
            chat_content += (
                f"<div class='message user-message'><p><strong>User:</strong> {msg.content}</p></div>"
            )
        else:
            chat_content += f"<div class='message'>Unknown Message Type: {msg}</div>"

    chat_content += "</div></body></html>"

    with open("chat.html", "w", encoding="utf-8") as html_file:
        html_file.write(chat_content)

    if st.button("Download Chat"):
        st.download_button("Download Chat", open("chat.html", "rb"), key="download_chat", file_name="chat.html",
                       mime="text/html")


def reset_lesson():
    st.session_state["messages"] = []
    st.session_state["completed_lessons"] = []
    st.session_state["current_lesson"] = None
    st.session_state["current_lesson_type"] = None
    st.session_state["code_snippet"] = None


def setup_page():
    st.set_page_config(page_title="LangChain: Getting Started Class", page_icon="🦜")
    st.title("🦜 LangChain: Getting Started Class")


# Main Streamlit Code
setup_page()

# Lesson selection dictionary
lesson_selection = st.sidebar.selectbox("Select Lesson", list(get_prompt.get_lesson_guide().keys()))

# Display lesson content and description based on selection
lesson_info = get_prompt.get_lesson_guide()[lesson_selection]

# Open the lesson file and decode it using UTF-8 encoding
with open(lesson_info["file"], encoding="utf-8") as f:
    lesson_content = f.read()

lesson_description = lesson_info["description"]

# Radio buttons for lesson type selection
lesson_type = st.sidebar.radio("Select Lesson Type", ["Instructions based lesson", "Interactive lesson with questions"])

# Clear chat session if dropdown option or radio button changes
if st.session_state.get("current_lesson") != lesson_selection or st.session_state.get(
        "current_lesson_type") != lesson_type:
    st.session_state["current_lesson"] = lesson_selection
    st.session_state["current_lesson_type"] = lesson_type
    st.session_state["messages"] = [AIMessage(
        content="Benvenuto! Sono AiDe, il tuo assistente virtuale che ti guiderà nell'apprendimento dell'ingegneria "
                "del software. Scrivimi un messaggio non appena sei pronto per iniziare!")]

# Display lesson name and description
st.markdown(f"**{lesson_selection}**")
st.write(lesson_description)

# Handle the messages and user's interaction
handle_messages()

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    run_langchain_model(prompt, lesson_type, lesson_content)

# Reset button for clearing the chat session
st.sidebar.button("Reset Lesson", on_click=reset_lesson)
download_chat()

