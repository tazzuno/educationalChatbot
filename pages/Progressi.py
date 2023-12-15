import streamlit as st
import time

st.title("Dashboard dello Studente")

if "completed_lessons" in st.session_state:
    st.subheader("Lezioni Svolte:")
    for lesson in st.session_state.completed_lessons:
        st.write(f"- {lesson}")
else:
    st.info("Nessuna lezione svolta finora.")

progresso = 0
bar = st.progress(progresso)

while True:
    progresso += 1
    time.sleep(1)


