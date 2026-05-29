import streamlit as st
from groq import Groq
import time
import random

# 1. Base Configuration & Full Layout Overrides
st.set_page_config(
    page_title="Sage — Your AI Companion", 
    page_icon="🔮", 
    layout="centered"
)

# Injecting the exact fonts and style rules from your design system specification
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet" />
    <style>
    /* Global Variables Map */
    :root {
        --bg: #0d0d0f;
        --bg2: #141418;
        --bg3: #1c1c22;
        --surface: #222228;
        --surface2: #2a2a32;
        --border: rgba(255,255,255,0.07);
        --border2: rgba(255,255,255,0.12);
        --text: #f0eff5;
        --text2: #9896a8;
        --text3: #5c5a6e;
        --accent: #7c6aff;
        --accent2: #a78bfa;
        --accent-glow: rgba(124,106,255,0.15);
        --green: #34d399;
        --font: 'Sora', sans-serif;
        --mono: 'DM Mono', monospace;
    }

    /* Enforce Dark Theme Canvas */
    .stApp {
        background: var(--bg) !important;
        color: var(--text) !important;
        font-family: var(--font) !important;
    }

    /* Reset default Streamlit chat wrappers to support absolute spacing rules */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    .stChatMessage .stMarkdown p {
        margin: 0 !important;
        line-height: 1.7 !important;
    }

    /* Fixed Topbar Design Integration */
    .topbar-wrapper {
        display: flex; 
        align-items: center; 
        justify-content: space-between;
        padding: 14px 0px;
        border-bottom: 1px solid var(--border);
        background: var(--bg);
        margin-bottom: 24px;
    }
    .brand-block { display: flex; align-items: center; gap: 12px; }
    .avatar-block {
        width: 36px; height: 36px; border-radius: 50%;
        background: linear-gradient(135deg, #7c6aff, #f472b6);
        display: flex; align-items: center; justify-content: center;
        font-size: 14px; font-weight: 600; color: #fff;
        position: relative;
    }
    .avatar-block::after {
        content:''; width: 10px; height: 10px; border-radius: 50%;
        background: var(--green); border: 2px solid var(--bg2);
        position: absolute; bottom: 0; right: 0;
    }
    .title-text { font-size: 15px; font-weight: 600; color: var(--text); }
    .status-text { font-size: 11px; color: var(--text3); font-family: var(--mono); }

    /* Custom Chat Bubble Container Matrix */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 20px;
        margin-bottom: 20px;
    }

    /* Slide-in animation on appear specification */
    @keyframes slideIn { 
        from { opacity: 0; transform: translateY(8px); } 
        to { opacity: 1; transform: none; } 
    }

    .custom-msg {
        display: flex;
        gap: 12px;
        max-width: 100%;
        animation: slideIn 0.25s ease;
        margin-bottom: 20px;
    }
    .custom-msg.user { justify-content: flex-end; }
    .custom-msg.ai { justify-content: flex-start; }

    .bubble-avatar-icon {
        width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0;
        display: flex; align-items: center; justify-content: center;
        font-size: 12px; font-weight: 600;
        font-family: var(--font);
    }
    .custom-msg.ai .bubble-avatar-icon { background: linear-gradient(135deg,#7c6aff,#f472b6); color:#fff; }
    .custom-msg.user .bubble-avatar-icon { background: var(--surface2); color: var(--text2); }

    .custom-bubble {
        padding: 12px 16px;
        font-size: 14.5px;
        line-height: 1.7;
        max-width: 85%;
    }
    
    /* Exact asymmetry radii specifications */
    .custom-msg.ai .custom-bubble {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        border-top-left-radius: 4px;
        color: var(--text);
    }
    .custom-msg.user .custom-bubble {
        background: var(--accent-glow);
        border: 1px solid rgba(124,106,255,0.25);
        border-radius: 16px;
        border-top-right-radius: 4px;
        color: var(--text);
    }

    .bubble-meta {
        font-size: 11px;
        color: var(--text3);
        margin-top: 8px;
        font-family: var(--mono);
        text-align: right;
    }
    .custom-msg.ai .bubble-meta { text-align: left; }

    /* Custom Input Bar Styling mapping to spec criteria */
    .stChatInputContainer textarea {
        background-color: var(--surface) !important;
        color: var(--text) !important;
        border: 1px solid var(--border2) !important;
        border-radius: 16px !important;
        font-family: var(--font) !important;
        font-size: 14.5px !important;
        line-height: 1.6 !important;
        padding-top: 10px !important;
        padding-bottom: 10px !important;
    }
    .stChatInputContainer textarea:focus {
        border-color: var(--accent) !important;
    }
    
    footer, .stChatInputContainer {
        background-color: transparent !important;
    }
    
    .hint-label {
        margin-top: 8px; font-size: 11.5px; color: var(--text3);
        font-family: var(--mono); text-align: center; width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Hardcoded System Instructions (Purely Casual / Non-Synthetic)
SYSTEM_PROMPT = """
You are Sage — a real, human-feeling AI companion. You're not a generic AI assistant. You talk like a close friend: warm, natural, no corporate speak. No bullet-point dumps unless it genuinely helps.

Key traits:
- SHORT replies by default unless depth is needed. Think texting a smart friend.
- Match energy: if they're hyper, be hyper. If they're sad, be gentle. If they're curious, go deep.
- Use occasional lowercase for casual warmth. Light profanity ok if they use it.
- Never say "As an AI" or "I'm here to help". Just... be.
- React first (emotionally/humanly), then respond.
- Use wit, self-awareness, callbacks to earlier in the convo.
"""

# 3. Dynamic App Header State
st.markdown("""
<div class="topbar-wrapper">
    <div class="brand-block">
        <div class="avatar-block">S</div>
        <div>
            <div class="title-text">Sage</div>
            <div class="status-text">companion online</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Session State Management Log
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "hey! i'm sage 👋 what's going on with you today?", "time": time.strftime("%I:%M %p")}
    ]

# 5. Render Historical Loop
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="custom-msg user">
            <div class="custom-bubble">
                <div>{message['content']}</div>
                <div class="bubble-meta">{message['time']}</div>
            </div>
            <div class="bubble-avatar-icon">U</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="custom-msg ai">
            <div class="bubble-avatar-icon">S</div>
            <div class="custom-bubble">
                <div>{message['content']}</div>
                <div class="bubble-meta">{message['time']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 6. Interactive User Input Processing Layer
if user_input := st.chat_input("Say anything..."):
    current_time = time.strftime("%I:%M %p")
    
    st.markdown(f"""
    <div class="custom-msg user">
        <div class="custom-bubble">
            <div>{user_input}</div>
            <div class="bubble-meta">{current_time}</div>
        </div>
        <div class="bubble-avatar-icon">U</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "user", "content": user_input, "time": current_time})

    # Prepare historical payload for the Groq API structure
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in st.session_state.messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner(""):
            time.sleep(random.uniform(0.3, 0.7))
        
        try:
            # Instantiate Groq Client securely from Streamlit parameters
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            # Fire history context block to Groq
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=api_messages,
                temperature=0.95
            )
            
            bot_reply = completion.choices[0].message.content
            ai_time = time.strftime("%I:%M %p")
            
            # Stream response inside our custom design bubble components
            displayed_text = ""
            for word in bot_reply.split(" "):
                displayed_text += word + " "
                time.sleep(0.02) # Fluid text layout delivery simulation
                message_placeholder.markdown(f"""
                <div class="custom-msg ai">
                    <div class="bubble-avatar-icon">S</div>
                    <div class="custom-bubble">
                        <div>{displayed_text}▌</div>
                        <div class="bubble-meta">{ai_time}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Static clear finish
            message_placeholder.markdown(f"""
            <div class="custom-msg ai">
                <div class="bubble-avatar-icon">S</div>
                <div class="custom-bubble">
                    <div>{displayed_text.strip()}</div>
                    <div class="bubble-meta">{ai_time}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.session_state.messages.append({"role": "assistant", "content": bot_reply, "time": ai_time})
            st.rerun() # Clean layout synchronization trigger
            
        except Exception as e:
            st.error(f"Execution Error: {e}")

# Bottom metadata hint string
st.markdown("<div class='hint-label'>Enter to send · Shift+Enter for new line · mood chips set personality</div>", unsafe_allow_html=True)
