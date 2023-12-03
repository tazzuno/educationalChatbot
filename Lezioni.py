import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import get_prompt
import chatbot_functions
from langchain.schema import AIMessage, HumanMessage
from StreamHandler import StreamHandler


def run_langchain_model(prompt, lesson_type, lesson_content):
    try:
        # Load the OpenAI API key from a .env file
        load_dotenv(find_dotenv('secrets.env'))
        openai_api_key = os.getenv("SECRET_KEY")

        # Set up a streaming handler for the model
        with st.chat_message("assistant"):
            stream_handler = StreamHandler(st.empty())
            model = ChatOpenAI(streaming=True, callbacks=[stream_handler], model="gpt-3.5-turbo",
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


# Main Streamlit Code
chatbot_functions.setup_page()

# Lesson selection dictionary
lesson_selection = st.sidebar.selectbox("Select Lesson", list(get_prompt.get_lesson_guide().keys()))

# Display lesson content and description based on selection
lesson_info = get_prompt.get_lesson_guide()[lesson_selection]
lesson_content = chatbot_functions.get_lesson_content(lesson_info["file"])
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
chatbot_functions.handle_messages()

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    run_langchain_model(prompt, lesson_type, lesson_content)

# Display code snippet if applicable
if "code_snippet" in st.session_state:
    chatbot_functions.display_code_snippet(st.session_state.code_snippet)

# Update lesson progress
chatbot_functions.update_progress(lesson_selection)