import streamlit as st
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from io import BytesIO
from PIL import Image
import time,re

genai.configure(api_key ="AIzaSyAy6LCRr1_ciWQn9dmp8K19X1mbsxyXj2s")


hf_api_key = "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"
hf_api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3-medium-diffusers"
hf_headers = {"Authorization": f"Bearer {hf_api_key}"}

def generate_gemini_response(prompt,temperature = 0.3):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt,generation_config = {"temperature":temperature})
        return response.text
    except Exception as e:
        print(f"exception occured {e}")

def generate_math_response( prompt :str,difficulty:str )-> str:
     try:
        system_prompt = "You are an Math mastermind! , skilled in :algebra,calculas,probability,surface&area,graphs,problems,sums,number theory etc. Always provide a step-by-step solution with ddetailed and clear explanation with final answer!"
        full_prompt = f"{system_prompt}\n Math problem solver{prompt}"
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt,generation_config = GenerationConfig(temperature = temperature))
        return generate_gemini_response(full_prompt)
     except Exception as e:
         return e


def is_safe_prompt(prompt: str) -> bool:
    forbidden = [
        "nude", "violence", "blood", "gun", "kill", "weapon", "drugs", "porn",
        "suicide", "abuse", "self-harm", "terror", "hate", "sex", "racism", "bomb"
    ]
    return not re.search("|".join(forbidden), prompt, re.IGNORECASE)

def generate_image(prompt: str) -> Image.Image:
    payload = {"inputs": prompt}
    response = requests.post(api_url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    if "image" in response.headers.get("Content-Type", ""):
        return Image.open(BytesIO(response.content))
    else:
        raise Exception("Response was not an image. Possible model error.")
    

# ======STRAMLIT UI======
st.set_page_config("🛠️ AI super app",layout ="centered")
st.st.title("🤖SMART AI")

tab1,tab2,tab3 = st.tabs("📐MATHS SOLVER!","🧠IMAGE GEN!","🗨️ai assistant!")

with tab1:
    st.header("Math problem solver!")
    with st.expander("examplebreakdown"):
        st.markdown("""
                   "calculas-  derivative of sin90",
                    geometry - find area of triangle (0,0,3,4)
                    algebra - x^2 + 5x +3 
                    probability - deck of 7 cards
                    """)
    with st.form("math.form",clear_on_submit = True):
           user_input = st.text_area("enter ur problem!",height = 100)
           difficulty = st.selectbox("level",["basic","intermidiate","advance"],1)
           submit = st.form_submit_button("SOLVE!")

    if submit and user_input.strip():
       prompt = f"[{difficulty} level]{user_input.strip()}"
       with st.spinner("Generatig response..."):
           answer = generate_math_response(prompt)
           st.success(answer)
           st.markdown(answer)
    else:
        st.warning("please enter a maths  question first!")

with tab2:
    st.header("🗨️ AI ASSISTANT!")
    user_input = st.text_input("ASK ANYTHING FROM SCIENCE , HISTORY ETC..")
    if st.button("get answer"):
        if user_input.strip():
             with st.spinner("Generatig response..."):
              answer = generate_gemini_response(user_input)
             st.success(answer)
             st.markdown(answer)
        else:
            st.warning("please enter a maths  question first!")
            

            