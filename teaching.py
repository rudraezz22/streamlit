import streamlit as st
import google.generativeai as genai


genai.configure(api_key = "AIzaSyAy6LCRr1_ciWQn9dmp8K19X1mbsxyXj2s")

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_response(prompt,temperature = 0.3):
    try:
        response = model.generate_content(prompt,generation_config = {"temperature":temperature})
        return response.text
    except Exception as e:
        print(f"exception occured {e}")


def setup_ui():
    st.title("AI teaching assistant")
    st.write("write the prompt")

    user_input = st.text_input("enter proompt")

    if user_input:
        st.write(f"your question was {user_input}")
        a = generate_response(user_input)
        st.write(f"your answer is {a}")
    else:
        st.write("enter a prompt again")


setup_ui()