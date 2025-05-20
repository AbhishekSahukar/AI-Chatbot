import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Function to get response from OpenRouter
def ask_mistral(messages):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "MyChatbot"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": messages
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "⚠️ Error: " + response.text

# Streamlit page config
st.set_page_config(page_title="AI Chatbot", layout="centered")
st.title("🤖 ChatGPT-style AI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# Display previous chat messages
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box at the bottom (just like ChatGPT)
user_prompt = st.chat_input("Type your message...")

if user_prompt:
    # Display user's message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Get assistant response
    bot_reply = ask_mistral(st.session_state.messages)

    # Display bot's response
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    # Save bot's message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
