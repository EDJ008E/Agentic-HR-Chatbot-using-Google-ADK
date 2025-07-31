import os
import streamlit as st
from utils.vector_store import VectorStoreManager
from tools import HRToolManager

# ----- Page Setup -----
st.set_page_config(page_title="HR Chatbot Assistant", layout="wide", page_icon="🤖")

# ----- Dummy user credentials -----
users = {
    "admin": "admin123",
    "user1": "password1",
    "Edwin": "123456",
}

# ----- Session Initialization 
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----- Login Page -----
def login_page():
    st.markdown("<h1 style='text-align: center;'>🔐 Login to HR Chatbot</h1>", unsafe_allow_html=True)
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if username in users and users[username] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

# ----- Load Vector DB & Tool Manager -----
@st.cache_resource
def initialize_tool_manager():
    os.environ["GOOGLE_API_KEY"] = ""  # Replace with real key or use st.secrets
    vector_manager = VectorStoreManager()
    if not vector_manager.load_vector_store():
        st.error("❌ Failed to load knowledge base. Please contact support.")
        st.stop()
    return HRToolManager(vector_manager.get_vector_db())

# ----- Chat Interface -----
def chatbot_page():
    st.markdown(f"<h1 style='text-align: center;'>🤖 HR Chatbot Assistant</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Welcome, <b>{st.session_state.username}</b>! Ask me about HR policies, leave, holidays, etc.</p>", unsafe_allow_html=True)

    # ----- Sidebar -----
    with st.sidebar:
        st.header("📌 Settings")
        st.markdown("**Ask questions like:**")
        st.markdown("- What is the leave policy?\n- Show holiday list\n- How to claim reimbursement?")

        # Show previous questions
        st.markdown("#### 🕘 Your Previous Questions:")
        recent_user_prompts = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
        if recent_user_prompts:
            for i, q in enumerate(recent_user_prompts[-5:], 1):
                st.markdown(f"{i}. {q}")
        else:
            st.markdown("_No previous questions yet._")

        # Clear and logout buttons
        if st.button("🔁 Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.messages = []
            st.rerun()

    # Load chatbot tools
    try:
        tool_manager = initialize_tool_manager()
    except Exception as e:
        st.error(f"❌ Initialization failed: {str(e)}")
        return

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input box
    prompt = st.chat_input("💬 Type your HR question here...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            response = tool_manager.process_query(prompt)
        except Exception as e:
            response = f"⚠️ Error: {str(e)}\nPlease contact HR or try again."

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# ----- App Flow -----
if not st.session_state.authenticated:
    login_page()
else:
    chatbot_page()
