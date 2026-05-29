import streamlit as st
from google import genai
import time
import random
import threading
import requests

# --- 1. THE AUTO-WAKE KEEP-ALIVE SYSTEM ---
def keep_alive(url):
    def ping():
        while True:
            try:
                requests.get(url)
                time.sleep(43200) # Keep app awake every 12 hours
            except:
                time.sleep(60)
    threading.Thread(target=ping, daemon=True).start()

# Change this to your live URL when deployed so it never hibernates!
YOUR_APP_URL = "https://your-app-name.streamlit.app"
keep_alive(YOUR_APP_URL)


# --- 2. THE DESIGN INSPIRED OVERRIDE ENGINE ---
st.set_page_config(
    page_title="Sage — Your AI Companion", 
    page_icon="🔮", 
    layout="centered"
)

# Deep clean integration of the custom CSS system variables from your template
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet" />
    <style>
    /* Global Variables Map */
    :root {
        --bg: #0d0d0f;
        --bg2: #141418;
        --border: rgba(255,255,255,0.07);
        --border2: rgba(255,255,255,0.12);
        --text: #f0eff5;
        --text2: #9896a8;
        --text3: #5c5a6e;
        --accent: #7c6aff;
        --accent2: #a78bfa;
        --accent-glow: rgba(124,106,255,0.15);
        --font: 'Sora', sans-serif;
    }

    /* Core App Structural Alignment */
    .stApp {
        background: var(--bg) !important;
        color: var(--text) !important;
        font-family: var(--font) !important;
    }

    /* Target the Chat Output Layout Blocks */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        padding: 4px 0px !important;
    }

    /* Overhaul input area to match look */
    .stChatInputContainer textarea {
        background-color: #222228 !important;
        color: var(--text) !important;
        border: 1px solid var(--border2) !important;
        border-radius: 16px !important;
        font-family: var(--font) !important;
    }
    
    .stChatInputContainer textarea:focus {
        border-color: var(--accent) !important;
    }

    /* Header Custom Components */
    .header-box {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 0px;
        border-bottom: 1px solid var(--border);
        margin-bottom: 25px;
    }
    
    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .custom-avatar {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: linear-gradient(135deg, #7c6aff, #f472b6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        color: white;
    }

    .brand-title {
        font-size: 16px;
        font-weight: 600;
        color: var(--text);
    }

    .brand-sub {
        font-size: 11px;
        color: var(--text3);
        font-family: 'DM Mono', monospace;
    }

    /* Mood Chips */
    .mood-container {
        display: flex;
        gap: 8px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }

    .custom-chip {
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        cursor: pointer;
        background: #141418;
        border: 1px solid var(--border);
        color: var(--text2);
        transition: all 0.2s ease;
    }
    
    .custom-chip.active {
        background: var(--accent-glow);
        border-color: var(--accent);
        color: var(--accent2);
    }
    </style>
""", unsafe_allow_html=True)


# --- 3. SESSION STATE CONFIGURATION ---
if "current_mood" not in st.session_state:
    st.session_state.current_mood = "auto"
if "user_context" not in st.session_state:
    st.session_state.user_context = ""
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "parts": ["hey! i'm sage 👋 what's going on with you today?"]}
    ]


# --- 4. HEADER RENDER ENGINE ---
st.markdown(f"""
<div class="header-box">
    <div class="brand">
        <div class="custom-avatar">S</div>
        <div>
            <div class="brand-title">Sage</div>
            <div class="brand-sub">{st.session_state.current_mood} mode active</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# --- 5. INTERACTIVE MOOD SELECTOR CHIPS ---
st.markdown("<p style='font-size:11px; color:#5c5a6e; font-family:\"DM Mono\"; margin-bottom:8px;'>SELECT PERSONALITY CHIP:</p>", unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)

moods = [
    ("🤖 Auto", "auto", col1),
    ("😂 Chill", "fun", col2),
    ("🫂 Warm", "support", col3),
    ("🧠 Nerd", "nerd", col4),
    ("🔥 Savage", "savage", col5)
]

for label, mood_id, col in moods:
    with col:
        is_active = "active" if st.session_state.current_mood == mood_id else ""
        if st.button(label, key=f"btn_{mood_id}"):
            st.session_state.current_mood = mood_id
            st.rerun()


# --- 6. OPTIONAL BACKDROP CONTEXT CONFIGURATION ---
with st.expander("⚡ Context Settings (Optional override)"):
    context_input = st.text_area("What's on your mind?", value=st.session_state.user_context, placeholder="e.g. I just had a rough day, tell me something funny...")
    if st.button("Save Context Layer"):
        st.session_state.user_context = context_input
        st.success("Context integrated into prompt matrix.")
        time.sleep(0.5)
        st.rerun()


# --- 7. DYNAMIC SYSTEM ENGINE SETUP ---
SYSTEM_BASE = """You are Sage — a real, human-feeling AI companion. You're not a generic AI assistant. You talk like a close friend: warm, natural, no corporate speak. No bullet-point dumps unless it genuinely helps.

Key traits:
- SHORT replies by default unless depth is needed. Think texting a smart friend.
- Match energy: if they're hyper, be hyper. If they're sad, be gentle. If they're curious, go deep.
- Use occasional lowercase for casual warmth. Light profanity ok if they use it.
- Never say "As an AI" or "I'm here to help". Just... be.
- React first (emotionally/humanly), then respond.
- Use wit, self-awareness, callbacks to earlier in the convo.
"""

MOOD_PROMPTS = {
    "auto": "Detect the emotional context from the message. Automatically switch between: funny & chill, warm & supportive, nerdy & deep, or witty & savage. You decide based on vibe.",
    "fun": "Mode: CHILL FRIEND. Be funny, use humor, keep it light and casual. Roast them gently if warranted. Short punchy replies.",
    "support": "Mode: SUPPORTIVE FRIEND. Be warm, empathetic, genuinely caring. Don't minimize feelings. Validate first, then gently help.",
    "nerd": "Mode: NERD FRIEND. Go deep on interesting topics. Use analogies, surprising facts, connect ideas. Love learning together.",
    "savage": "Mode: WITTY & SAVAGE. Sharp humor, clever comebacks, roasting with love. Never cruel, always clever. Sarcasm welcome."
}

# Combine rules for Gemini configuration block
active_system_prompt = SYSTEM_BASE + "\n\n" + MOOD_PROMPTS[st.session_state.current_mood]
if st.session_state.user_context:
    active_system_prompt += f"\n\nUser Context configuration: {st.session_state.user_context}"


# --- 8. LIVE CHAT LIST GENERATOR ---
for message in st.session_state.messages:
    st_role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(st_role):
        st.write(message["parts"][0])


# --- 9. INTERACTIVE REAL-TIME INPUT THREAD ---
if user_chat := st.chat_input("Say anything..."):
    # Render user message inside UI block immediately
    with st.chat_message("user"):
        st.write(user_chat)
    
    st.session_state.messages.append({"role": "user", "parts": [user_chat]})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Micro-delay simulation mimicking the template's bounce animation
        with st.spinner(""):
            time.sleep(random.uniform(0.3, 0.8))
        
        try:
            # Instantiate client safely from Streamlit variables
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
            
            # Fire data to Gemini Core
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=st.session_state.messages,
                config=genai.types.GenerateContentConfig(
                    system_instruction=active_system_prompt,
                    temperature=0.95
                )
            )
            
            bot_response = response.text
            
            # Smooth custom typewriter loop mapping to your smooth scroll layout
            displayed_text = ""
            for word in bot_response.split(" "):
                displayed_text += word + " "
                time.sleep(0.025)
                message_placeholder.write(displayed_text + "▌")
            
            message_placeholder.write(displayed_text.strip())
            
            # Append final output cleanly to state loop
            st.session_state.messages.append({"role": "model", "parts": [bot_response]})
            
        except Exception as e:
            st.error(f"Engine Exception Error: {e}")
