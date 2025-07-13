import streamlit as st
import google.generativeai as genai

genai.configure(api_key = "AIzaSyAy6LCRr1_ciWQn9dmp8K19X1mbsxyXj2s")

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_response(prompt):
    try:
      response = model.generate_content(prompt)
      return response.text
    except Exception as e:
       print(e)
       
st.set_page_config(page_title = "AI Teachin Assistant!",layout = "centered")
st.title("Ai teaching assistant")
st.write("ask me anything and get answers!")

if "history" not in st.session_state:
   st.session_state.history = []

if st.button("clear chat"):
   st.session_state.history = []
   st.rerun()

user_input = st.text_input("ask the question!")

if st.button("ask!"):
   if user_input.strip():
      with st.spinner("GENERATING....!"):
         answer = generate_response(user_input.strip())
         st.session_state.history.append({"question":user_input.strip(),"answer":answer})
   else:
      st.warning("enter a question first!")

st.markdown("""
<style>
            .history{
            max-height : 300px;
            overflow-y:auto;
            border:8px solid grey;
            padding:10px;
            background-color:black;
            border-radius:8px;
            font-family:Arial,sans-serif;
            }
            .question{
            font-weight:bold;
            color:white;
            margin:12px;

            }
            .answer{
            color:white,
            margin-bottom:16px;
            white-space :pre-wrap
            }

            </style>
            """,unsafe_allow_html = True)


history_html = "<div class = 'history'>"
for idx , qa in enumerate(st.session_state.history,1):
   q = qa["question"]
   a = qa["answer"]
   history_html += f"<div class = 'question'> Q{idx}:{q}<br></div>"
   history_html += f"<div class = 'answer'> A{idx}:{a}<br></div>"

history_html += "</div>"

st.markdown(history_html,unsafe_allow_html = True)


