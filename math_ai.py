import google.generativeai as genai
from google.generativeai.types import GenerationConfig
import io
import streamlit as st

api_key = "AIzaSyAy6LCRr1_ciWQn9dmp8K19X1mbsxyXj2s"

genai.configure(api_key = api_key)

def generate_response( prompt :str,temperature:float = 0.3 )-> str:
     try:
        system_prompt = "You are an Math mastermind! , skilled in :algebra,calculas,probability,surface&area,graphs,problems,sums,number theory etc. Always provide a step-by-step solution with ddetailed and clear explanation with final answer!"
        full_prompt = f"{system_prompt}\n Math problem solver{prompt}"
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt,generation_config = GenerationConfig(temperature = temperature))
        return response.text
     except Exception as e:
         return e
     
def setup_ui():
    st.set_page_config("Math Mastermind!",layout = "centered")
    st.title("Math problem solver")
    st.write("Solve problem and get higher precision!")

    with st.expander("examplebreakdown"):
        st.markdown("""
                   "calculas-  derivative of sin90",
                    geometry - find area of triangle (0,0,3,4)
                    algebra - x^2 + 5x +3 
                    probability - deck of 7 cards
                    """)
        with st.form("math.form",clear_on_submit = True):
           user_input = st.text_area("enter ur problem!",height = 100)
           col1,col2 = st.columns([3,1])
           with col1:
               submit = st.form_submit_button("SOLVE!")
           with col2:
               difficulty = st.selectbox("level",["basic","intermidiate","advance"],1)

    if "history" not in st.session_state:
        st.session_state.history = []
    if submit and user_input.strip():
       prompt = f"[{difficulty} level]{user_input.strip()}"
       with st.spinner("Generatig response..."):
           answer = generate_response(prompt)
       st.session_state.history.insert(0,{
           "question":user_input.strip(),
           "answer":answer,
           "difficulty":difficulty
       })
       st.rerun()
    elif submit:
        st.warning("please enter a maths  question first!")

    col_clear,col_export = st.columns(2)
    with col_clear:
        if st.button("clear_history"):
            st.session_state.history = []
            st.rerun()
    with col_export:
        if st.session_state.history:
            text = "\n\n ".join(f"Q{idx+1}: {qa['question']} \n A{idx+1} : {qa['answer']}" for idx,qa in enumerate(st.session_state.history) )
            st.download_button("download_solution",data = text,file_name = "data.txt")
    if st.session_state.history:
        st.markdown("solution history")
        for i , qa in enumerate(st.session_state.history):
            st.markdown(f"Q{i+1}({qa['difficulty']}): {qa['question']}")
            st.markdown(f"\n Answer :({qa['answer']})")

setup_ui()
            
            

