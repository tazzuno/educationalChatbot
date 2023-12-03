import streamlit as st
import chatbot_functions as cf

st.title("Dashboard dello Studente")

if "completed_lessons" in st.session_state:
    st.subheader("Lezioni Svolte:")
    for lesson in st.session_state.completed_lessons:
        st.write(f"- {lesson}")
else:
    st.info("Nessuna lezione svolta finora.")
