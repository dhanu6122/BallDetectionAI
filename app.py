import streamlit as st

st.title("Ball Detection AI 🔴")

# Simple login system
USER_CREDENTIALS = {
    "user1": "pass123",
    "judge": "hack2026"
}

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if username not in USER_CREDENTIALS or USER_CREDENTIALS[username] != password:
    st.warning("Please enter correct credentials")
    st.stop()

st.success("Login successful!")