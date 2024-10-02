import os
import io
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

#sets the avatar for user as well as the bot
USER_AVATAR = "👤"
BOT_AVATAR = "✨"
image_path = "Google-Gemini-AI-Logo.png"
#private key for gemini.
private_key = "AIzaSyBBdPPHB8e7h6u0lr1-nKMiB80MGzlSvlk"
genai.configure(api_key=private_key)


#conifgs the bar 
st.set_page_config(
    page_title = "Gemini",
    page_icon=":sparkle",
    layout="centered"
)

#side bar components
with st.sidebar:
    st.image(image_path , width = 200)
    select_model = st.sidebar.selectbox('Choose a Model' , ['gemini-pro' , 'gemini-pro-vision'] , key='select_model')
    if select_model == 'gemini-pro':
        model = genai.GenerativeModel('gemini-pro')
    if select_model == 'gemini-pro-vision':
        model_vision = genai.GenerativeModel('gemini-pro-vision')

#role swap after every prompt
def role_swap(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

#initialising chat.
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    initial_prompt = "How can i help you today?"
    st.chat_message("assistant" , avatar = BOT_AVATAR).markdown(initial_prompt)

#clearing the chat history
def clear_chat():
    initial_prompt = "How can i help you today?"
    st.session_state.chat_session = model.start_chat(history=[])
    st.chat_message("assistant" , avatar = BOT_AVATAR).markdown(initial_prompt)
st.sidebar.button('Clear Chat Histrory',on_click=clear_chat) 

#displays the history accordingly
for message in st.session_state.chat_session.history:
    with st.chat_message(role_swap(message.role),avatar=BOT_AVATAR if message.role == "model" else USER_AVATAR):
        st.markdown(message.parts[0].text)

#main prompt logic.
user_prompt = st.chat_input("Message Gemini")
if user_prompt:
    st.chat_message("user",avatar=USER_AVATAR).markdown(user_prompt)
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    with st.chat_message("assistant",avatar=BOT_AVATAR):
        st.markdown(gemini_response.text)
