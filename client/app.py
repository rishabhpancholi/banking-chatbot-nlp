import streamlit as st
import streamlit.components.v1 as components
import requests

#For wide layout
st.set_page_config(
    layout="wide"
)

#API url
url = 'https://banking-chatbot-nlp.onrender.com/'

#Initialize session state
if "logged_in" not in st.session_state:
   st.session_state.logged_in = False
   st.session_state.username = ""
   st.session_state.password = ""
   st.session_state.chats = []

#Navigation
tab1, tab2 = st.tabs(["Home", "Chat"])

#Home page
with tab1:
    st.title("🏦 BankingFAQ Chatbot 🤖")
    st.subheader("💬 Ask your basic banking queries here!")

    st.markdown(
                """
                     <div style="font-size: 1.5rem; margin: 3rem 0;">
                        👋 Welcome to the <strong>BankingFAQ ChatBot</strong> interface — a smart, user-friendly platform built to offer you personalized customer support with ease. <br><br>
                        🤖 This intelligent chatbot uses natural language processing and machine learning to simulate a virtual banking assistant, helping you with common banking questions and concerns efficiently. 💡
                    </div>
                """, unsafe_allow_html=True
                )

  # Chat page
with tab2:
    st.title("💬 Chat with BankingFAQ Bot")
    if not st.session_state.logged_in:
        st.subheader("Login/Signup/Delete")

        tab1,tab2,tab3 = st.tabs(["Login","Signup","Delete"])

        with tab1:

            username = st.text_input("username",placeholder = "enter your username",key="login_username")
            password = st.text_input("password",type="password", placeholder = "enter your password",key="login_password")

            login_button = st.button("Login",key="login_button")

            if login_button:
                try:
                   response = requests.post(f'{url}/login',json={"username":username,"password":password})
                   if response.status_code ==200:
                      data = response.json()
                      st.session_state.logged_in = True
                      st.session_state.username = username
                      st.session_state.password = password
                      st.session_state.chats = data.get("user_chats")
                      st.rerun()
                        
                   else:
                      st.error("Invalid username or password")
                except Exception as e:
                      st.error(e)

        with tab2:
            username = st.text_input("username",placeholder = "enter your username",key = "signup_username")
            password = st.text_input("password",type="password", placeholder = "enter your password",key="signup_password")

            signup_button = st.button("Signup",key="signup_button")

            if signup_button:
                try:
                    response = requests.post(f'{url}/signup',json={"username":username,"password":password})
                    if response.status_code ==200:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.password = password
                        st.rerun()

                    else:
                        st.error("Username not available")
                except Exception as e:
                    st.error(e)

        with tab3:
            username = st.text_input("username",placeholder = "enter your username",key = "delete_username")
            password = st.text_input("password",type="password", placeholder = "enter your password",key="delete_password")

            delete_button = st.button("Delete",key="delete_button")

            if delete_button:
                try:
                    response = requests.delete(f'{url}/delete',json={"username":username,"password":password})
                    if response.status_code ==200:
                        st.session_state.logged_in = False
                        st.session_state.username = ""
                        st.session_state.password = ""
                        st.success("Account deleted successfully")
                        st.rerun()

                    else:
                        st.error("Username not available")
                except Exception as e:
                    st.error(e)

    else:
       st.subheader(f"Welcome, {st.session_state.username}!")

       user_input = st.text_input("Enter your query here")


       if st.button("Send") and user_input:
          try:
             response = requests.post(f'{url}/respond',json={"user":{"username":st.session_state.username,"password":st.session_state.password},"chat":{"user_input":user_input}})
             if response.status_code == 200:
                    data = response.json()
                    chatbot_response = data.get("message")
                    st.session_state.chats.append({"user_input": user_input,"chatbot_response":chatbot_response})

                    #Input box
                    chat_box_html = '<div style = "padding: 1rem; border: 0.1rem solid green; border-radius: 0.5rem;">'

                    for chat in reversed(st.session_state.chats):
                      chat_box_html+= f"""
                           <div style="background-color: white; padding: 0.5rem; margin: 1rem; color: black; font-weight:bolder; border-radius: 0.5rem;"><strong>You</strong>: {chat.get("user_input")}</div>
                           <div style="background-color: white; padding: 0.5rem; margin: 1rem; color: black; font-weight:bolder; border-radius: 0.5rem;"><strong>Bot</strong>: {chat.get("chatbot_response")}</div>
                           <div style = "height: 1rem;"></div>
                          """
        
                    chat_box_html+= '</div>'
    
                    components.html(chat_box_html,scrolling=True,height=500)

                   
                    st.markdown('<div style = "height: 2rem;"></div>',unsafe_allow_html=True)   
             else:
                    st.error("Something went wrong")
          except Exception as e:
                st.error(e)

       #Logout
       if st.button("Logout"):
          st.session_state.logged_in = False
          st.session_state.username = ""
          st.session_state.chats = []
          st.rerun()








                
            


