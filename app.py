# app.py (project root)
import os
import sys
import streamlit as st
from time import perf_counter

# Ensure we can import from ./src
SRC_DIR = os.path.join(os.path.dirname(__file__), "src") # src/.
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)
    
# Import shared logger
from src.config.logging_config import logger
logger.info("[APP] logging_config imported successfully.")
logger.debug("[APP] Streamlit started with DEBUG logging enabled")
# --- Robust import: accept both class name variants ---
def load_bot_class():
    try:
        from src.utils.chatbot_agentic_v3 import Chatbot_v3 as BotClass
        logger.info("[APP] Loaded Chatbot_v3 from utils.chatbot_agentic_v3")
        return BotClass
    except Exception:
        from importlib import import_module
        mod = import_module("utils.chatbot_agentic_v3")
        for name in ("ChatbotAgenticV3", "Chatbot", "Chatbot_v3"):
            if hasattr(mod, name):
                logger.info("[APP] Loaded %s from utils.chatbot_agentic_v3", name)
                return getattr(mod, name)
        logger.error(
            "[APP] Could not find a chatbot class in utils.chatbot_agentic_v3.py"
        )
        raise ImportError(
            "Couldn't find Chatbot_v3 / ChatbotAgenticV3 / Chatbot "
            "in utils.chatbot_agentic_v3.py"
        )

BotClass = load_bot_class()

st.set_page_config(page_title="MemoriAI MVP", page_icon="🧠", layout="centered")
st.title("MemoriAI – MVP (Use Case 1)")
st.caption("SQL Profile + Vector DB + LLM (Ollama).")

logger.info("[APP] Streamlit UI started")

@st.cache_resource(show_spinner=False)
def get_bot():
    logger.info("[APP] Chatbot instance created (cache_resource)")
    return BotClass()

if "history" not in st.session_state:
    st.session_state.history = []

# Show history
for role, msg in st.session_state.history:
    with st.chat_message(role):
        st.markdown(msg)

# Input
user_msg = st.chat_input("Ask me something...")
if user_msg:
    logger.info("[APP] New user message received (length=%d)", len(user_msg))

    st.session_state.history.append(("user", user_msg))
    with st.chat_message("user"):
        st.markdown(user_msg)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            bot = get_bot()
            t0 = perf_counter()
            reply = bot.chat(user_msg)
            elapsed = perf_counter() - t0
            logger.info(
                "[APP] Model reply generated in %.2f seconds (len=%d)",
                elapsed,
                len(reply),
            )
            st.markdown(reply)

    st.session_state.history.append(("assistant", reply))
