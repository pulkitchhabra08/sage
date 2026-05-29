import streamlit as st
from groq import Groq

st.set_page_config(page_title="Sage", page_icon="🌿", layout="centered")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are Sage — a real, human-feeling AI companion. 
You talk like a close friend: warm, natural, no corporate speak. 
Short replies by default unless depth is needed. Match energy: 
if they're hyper be hyper, if sad be gentle, if curious go deep. 
Never say 'As an AI'. React humanly first, then respond. 
Use wit, callbacks to earlier in the convo. No bullet dumps."""

st.title("🌿 Sage")
st.caption("your AI companion")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "hey! what's going on with you today?"
    })

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("say anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(""):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages,
                temperature=0.92,
                max_tokens=800
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.write(reply)
