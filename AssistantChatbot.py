from google import genai
import streamlit as st
from googlesearch import search

# Page Config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# Load HTML UI
def load_ui():
    with open("ui.html", "r", encoding="utf-8") as f:
        return f.read()

# Show UI
st.markdown(load_ui(), unsafe_allow_html=True)

# Gemini Client
client = genai.Client(api_key="API_KEY")

# Initialize states

if "history" not in st.session_state:
    st.session_state.history = []

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None


# FORM

with st.form("chat_form", clear_on_submit=True):

    user_input = st.text_input("💬 Ask Anything")

    submitted = st.form_submit_button("🚀 Ask AI")


# Generate Response

if submitted and user_input:

    # Move old current chat to history
    if st.session_state.current_chat is not None:
        st.session_state.history.append(
            st.session_state.current_chat
        )

    
    # Build Conversation Memory

conversation = ""

# Add old chats from history
for old_user, old_ai in st.session_state.history:

    conversation += f"User: {old_user}\n"
    conversation += f"AI: {old_ai}\n"

# Add current chat too
if st.session_state.current_chat is not None:

    current_user, current_ai = st.session_state.current_chat

    conversation += f"User: {current_user}\n"
    conversation += f"AI: {current_ai}\n"

# Add latest user question
conversation += f"User: {user_input}"

# GOOGLE SEARCH RESULTS

search_results = ""

try:

    results = list(search(user_input, num_results=5))

    for r in results:
        search_results += r + "\n"

except:
    search_results = "No web results found."


# FINAL PROMPT

final_prompt = f"""
You are a helpful AI assistant.

Conversation History:
{conversation}

User Question:
{user_input}

Relevant Web Results:
{search_results}

Answer clearly and accurately.
"""

# AI Response

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=final_prompt
)

    # Save latest chat
st.session_state.current_chat = (
        user_input,
        response.text
    )


# SHOW CURRENT CHAT

if st.session_state.current_chat:

    user_msg, ai_msg = st.session_state.current_chat

    st.markdown(f"""
    <div class="chat-box user">
        <b>🧑 You:</b><br>{user_msg}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="chat-box ai">
        <b>🤖 AI:</b><br>{ai_msg}
    </div>
    """, unsafe_allow_html=True)


# HISTORY SECTION

with st.expander("📜 Chat History"):

    for user_msg, ai_msg in reversed(st.session_state.history):

        st.markdown(f"""
        <div class="chat-box user">
            <b>🧑 You:</b><br>{user_msg}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="chat-box ai">
            <b>🤖 AI:</b><br>{ai_msg}
        </div>
        """, unsafe_allow_html=True)