# Functions
import streamlit as st
from langchain.schema import HumanMessage, AIMessage


@st.cache_data()
def get_lesson_content(lesson_file):
    try:
        with open(lesson_file, "r") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Error: Lesson file not found at {lesson_file}")
        st.stop()


def display_code_snippet(code_block):
    st.code(code_block, language="python")


def update_progress(lesson_selection):
    if "completed_lessons" not in st.session_state:
        st.session_state.completed_lessons = []
    if lesson_selection not in st.session_state.completed_lessons:
        st.session_state.completed_lessons.append(lesson_selection)


def setup_page():
    st.set_page_config(page_title="LangChain: Getting Started Class", page_icon="🦜")
    st.title("🦜 LangChain: Getting Started Class")


def handle_messages():
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for msg in st.session_state["messages"]:
        if isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)
        else:
            st.chat_message("assistant").write(msg.content)