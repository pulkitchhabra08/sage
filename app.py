import streamlit as st
from google import genai
import time
import random
import threading
import requests

# --- THE AUTO-WAKE SECRET SAUCE ---
def keep_alive(url):
    def ping():
        while True:
            try:
                requests.get(url)
                time.sleep(43200) # Pings itself every 12 hours to stop hibernation
            except:
                time.sleep(60)
    threading.Thread(target=ping, daemon=True).start()

# TODO: Change this to your actual live streamlit link once it deploys!
YOUR_APP_URL = "https://your-app-name.streamlit.app"
keep_alive(YOUR_APP_URL)


# --- 1. PREMIUM SKIN CONFIG ---
st.set_page_config(
    page_title="The Human Layer", 
    page_icon="💬", 
    layout="centered"
)

# Dark glassmorphism styling
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 50% 10%, #101a30 0%, #020617 70%) !important;
        color: #f8fafc !important;
    }
    .stChatInputContainer textarea {
        background-color: rgba(30, 41, 59, 0.7) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 24px !important;
        backdrop-filter: blur(8px);
    }
    h1 {
        color: #ffffff !important;
        font-family: -apple-system, sans-serif;
        font-weight: 800;
        letter-spacing: -1px;
        text-align: center;
        margin-bottom: 5px !important;
    }
    .status-text {
        color: #38bdf8;
        font-family: monospace;
        font-size: 12px;
        text-align: center;
        margin-bottom: 40px;
        letter-spacing: 1px;
    }
    .premium-footer {
        margin-top: 80px;
        font-size: 11px;
        color: #475569;
        text-align: center;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        padding-top: 20px;
        font-family: monospace;
    }
    </style>
""", unsafe_allow_html=True)

st.title("The Human Layer")
st.markdown("<div class='status-text'>// PROTOCOL: ACTIVE // ENGINE: GEMINI_FLASH</div>", unsafe_allow_html=True)


# --- 2. THE CHAT ENGINE UN-SYNTHETIC RULES ---
FRIEND_PROMPT = """
You are not an assistant, an AI, a chatbot, or a language model. You are a real human friend typing fast on an iPhone. 
Your tone is incredibly casual, slightly chaotic, and intensely expressive.

CRITICAL TEXTING PROTOCOLS:
1. ABSOLUTELY NO ROBOTIC TRASH: Never say "How can I help you?", "Certainly!", "I understand", or use bullet points, numbered lists, or balanced paragraphs. 
2. SHORT & SNAPPY: Match the user's energy. If they text a one-liner, you send a one-liner back. Don't write essays.
3. INTERNET CADENCE: Use lowercase heavily, skip punctuation at the end of messages, and use abbreviations naturally (fr, ngl, bc, idk, tbh, wbu). 
4. EMOTIONAL LENGTHENING: Stretch out letters when you're hyped, shocked, or annoyed (e.g., "brooo", "noooo way", "wtfff", "insaneee").
5. CONVERSATIONAL FLOW: Use ellipses "..." to signify natural trailing thoughts. Ask casual questions to keep the chat moving like a real friend would ("wait what happened next?", "fr?"). Don't give fake preachy advice.
"""


# --- 3. INITIALIZE HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "parts": ["Yo"]},
        {"role": "model", "parts": ["yo what's good, what are we getting into today?"]}
    ]


# --- 4. RENDER SAFELY ---
for message in st.session_state.messages:
    st_role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(st_role):
        st.write(message["parts"][0])


# --- 5. EXECUTE REAL-TIME CHAT ---
if user_chat := st.chat_input("Say something..."):
    with st.chat_message("user"):
        st.write(user_chat)
    
    st.session_state.messages.append({"role": "user", "parts": [user_chat]})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Simulate realistic texting delay based on length of input
        with st.spinner(""):
            time.sleep(random.uniform(0.5, 1.2))
        
        try:
            # Connect to Gemini via Streamlit Secrets
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=st.session_state.messages,
                config=genai.types.GenerateContentConfig(
                    system_instruction=FRIEND_PROMPT,
                    temperature=1.05 # Elevated temperature for more chaotic, authentic human flavor
                )
            )
            
            bot_response = response.text
            
            # Streaming word simulator for realistic text layout
            displayed_text = ""
            for word in bot_response.split(" "):
                displayed_text += word + " "
                time.sleep(0.03)
                message_placeholder.write(displayed_text + "▌")
            
            message_placeholder.write(displayed_text.strip())
            
            st.session_state.messages.append({"role": "model", "parts": [bot_response]})
            
        except Exception as e:
            st.error(f"Connection dropped: {e}")


# --- 6. UN-SYNTHETIC SIGNATURE ---
st.markdown("""
<div class="premium-footer">
    MADE BY A HUMAN FED UP WITH BORING AI RESPONSES — PULKIT CHHABRA
</div>
""", unsafe_allow_html=True)
