import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL")
CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Fetch all pages (same as before)
def fetch_all_pages_from_space(space_key):
    all_docs = []
    start = 0
    limit = 50

    while True:
        url = f"{BASE_URL}/rest/api/content"
        params = {
            "type": "page",
            "spaceKey": space_key,
            "limit": limit,
            "start": start,
            "expand": "body.storage"
        }
        response = requests.get(
            url,
            auth=HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_TOKEN),
            headers={"Accept": "application/json"},
            params=params
        )
        response.raise_for_status()
        data = response.json()
        pages = data.get("results", [])

        if not pages:
            break

        for page in pages:
            title = page.get("title", "No Title")
            html_content = page["body"]["storage"]["value"]
            soup = BeautifulSoup(html_content, "html.parser")
            text_content = soup.get_text(separator="\n", strip=True)
            all_docs.append(f"\n\n## {title}\n{text_content}")

        if len(pages) < limit:
            break
        start += limit

    return "\n".join(all_docs)

def ask_together_ai(question, context):
    endpoint = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": f"You are a helpful assistant based on this documentation:\n{context}"},
            {"role": "user", "content": question}
        ],
        "temperature": 0.3,
        "max_tokens": 300
    }

    response = requests.post(endpoint, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

# UI part with Streamlit


# --- UI Layout ---
st.set_page_config(page_title="Confluence AI Agent", page_icon="🤖", layout="wide")


# Sidebar with logo, info, and collapsible chat history
with st.sidebar:
    st.image("ai_logo.png", width=140)
    st.markdown("<h2 style='color:#0072C6;'>Confluence AI Agent</h2>", unsafe_allow_html=True)
    st.write("<span style='color:#444;'>Ask questions based on your Confluence space documentation.</span>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h4 style='color:#0072C6;'>Previous Q&A</h4>", unsafe_allow_html=True)
    if st.session_state.get("chat_history"):
        for idx, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
            with st.expander(f"Q{idx}: {q}"):
                st.markdown(f"<span style='color: #555; font-size: 13px;'><b>AI:</b> {a}</span>", unsafe_allow_html=True)


# Main area
st.markdown("<h1 style='color:#0072C6; text-align:center;'>🤖 Confluence AI Agent</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#444;'>Your smart assistant for Confluence documentation</div>", unsafe_allow_html=True)

# Chat history state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Load docs only once
if 'docs' not in st.session_state:
    with st.spinner("Loading Confluence content... This might take a few seconds."):
        st.session_state.docs = fetch_all_pages_from_space(SPACE_KEY)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#0072C6;'>Ask your question:</h4>", unsafe_allow_html=True)
user_question = st.text_input("Type your question here...", key="user_input")



# Custom CSS for Streamlit button
st.markdown('''
    <style>
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #0072C6 0%, #00C6D7 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75em 2em;
        font-size: 1.1em;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        cursor: pointer;
        transition: transform 0.1s, box-shadow 0.1s;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) scale(1.04);
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }
    </style>
''', unsafe_allow_html=True)


col_btn, col_space = st.columns([1, 3])
with col_btn:
    if st.button("Ask AI Agent"):
        if not user_question:
            st.warning("Please enter a question first.")
        else:
            with st.spinner("Getting answer from AI..."):
                try:
                    answer = ask_together_ai(user_question, st.session_state.docs)
                    st.session_state.chat_history.append((user_question, answer))
                    st.success("Answer received!")
                except Exception as e:
                    st.error(f"Error getting answer: {e}")

st.markdown("<div style='margin-top: 30px; color:#888;'>Powered by <b>AI Agent InHouse</b></div>", unsafe_allow_html=True)

# Display chat history in main area (last 5 Q&A)
if st.session_state.chat_history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#0072C6;'>Recent Q&A</h4>", unsafe_allow_html=True)
    # Show only the most recent Q&A
    q, a = st.session_state.chat_history[-1]
    st.markdown(f"<span style='color:#0072C6;'><b>Q:</b></span> {q}", unsafe_allow_html=True)
    st.markdown(f"<span style='color: #555; font-size: 13px;'><b>AI:</b> {a}</span>", unsafe_allow_html=True)
