import asyncio
import streamlit as st
from agent.agent_config import run_agent
from vector_store import save_to_vectorstore
from auth import create_usertable, add_user, login_user
# Remove this (WRONG):
from agents import Agent
from openai import AsyncOpenAI

# Initialize the user table
create_usertable()

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if choice == "Login":
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type='password')
    if st.sidebar.button("Login"):
        result = login_user(username, password)
        if result:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid username or password")

elif choice == "Sign Up":
    st.sidebar.subheader("Create Account")
    new_user = st.sidebar.text_input("New Username")
    new_password = st.sidebar.text_input("New Password", type='password')
    if st.sidebar.button("Sign Up"):
        add_user(new_user, new_password)
        st.success("Account created. Please login.")

# Show AI Assistant only if user is logged in
if st.session_state.logged_in:
    st.write(f"👋 Hello, **{st.session_state.username}**!")

    # 👇 Educational Agent Initialization
    st.title("AI Educational Assistant")
    st.info("📚 Initializing notes into vector database...")
    save_to_vectorstore()

    # Test input
    question = st.text_input("Ask a question from your syllabus", "Explain the laws of motion from unit 3.")
    if st.button("Ask"):
        with st.spinner("Thinking..."):
            answer = asyncio.run(run_agent(question))
            st.success("Answer:")
            st.write(answer)
