import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import get_prompt
from langchain.schema import AIMessage, HumanMessage
from StreamHandler import StreamHandler


def handle_messages():
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for msg in st.session_state["messages"]:
        if isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)
        else:
            st.chat_message("assistant").write(msg.content)


def run_langchain_model(prompt, lesson_type, lesson_content):
    try:
        # Load the OpenAI API key from a .env file
        load_dotenv(find_dotenv('secrets.env'))
        openai_api_key = os.getenv("SECRET_KEY")

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
lesson_content = get_lesson_content(lesson_info["file"])
lesson_description = lesson_info["description"]

# Radio buttons for lesson type selection
lesson_type = st.sidebar.radio("Select Lesson Type", ["Instructions based lesson", "Interactive lesson with questions"])

# Clear chat session if dropdown option or radio button changes
if st.session_state.get("current_lesson") != lesson_selection or st.session_state.get(
        "current_lesson_type") != lesson_type:
    st.session_state["current_lesson"] = lesson_selection
    st.session_state["current_lesson_type"] = lesson_type
    st.session_state["messages"] = [AIMessage(
        content="Welcome! This short course will help you get started with LangChain. Let me know when you're all set "
                "to jump in!")]

# Display lesson name and description
st.markdown(f"**{lesson_selection}**")
st.write(lesson_description)

# Message handling and interaction
handle_messages()

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    run_langchain_model(prompt, lesson_type, lesson_content)

download_chat()
st.sidebar.button("Reset Lesson", on_click=reset_lesson)
