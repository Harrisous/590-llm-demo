import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone
from datetime import datetime

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "financials"
index = pc.Index(index_name)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Streamlit app configuration
st.set_page_config(page_title="Ask Financials", page_icon="🤖", layout="wide")

# CSS for sticky title and scrollable chat history
st.markdown(
    """
    <style>
    /* Sticky title */
    .title-container h1 {
        text-align: center;
        color: black;
        background-color: white;
        margin: 0;
    }

    /* Scrollable chat history */
    .chat-history {
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
    }

    /* Focus on input box */
    input[type="text"] {
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sticky title
with st.container():
    st.markdown('<div class="title-container"><h1>Ask Financials</h1></div>', unsafe_allow_html=True)

# Initialize session state for chat history and input box
if "messages" not in st.session_state:
    st.session_state.messages = []
if "input_box" not in st.session_state:
    st.session_state.input_box = ""

# Callback function to handle user input submission
def submit_query():
    user_query = st.session_state.input_box.strip()
    if user_query:
        st.session_state.input_box = ""
        # Use the bottom spinner placeholder
        with st.session_state.spinner_placeholder.spinner("Generating..."):
            st.session_state.messages.append({"role": "user", "content": user_query})
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            response = client.embeddings.create(
                model="text-embedding-ada-002",
                input=user_query,
                encoding_format="float"
            )
            embedding = response.data[0].embedding
            res = index.query(vector=embedding, top_k=5, include_metadata=True)
            context = "\n".join([str(match["metadata"]) for match in res["matches"]])
            prompt = f"""
            You are an AI assistant that answers questions based on provided context. The overall answer style should be financial, and you will not answer anything unrelated.
            Today's date is {current_date}.
            Here is some context:\n{context}
            Current Question: {user_query}
            Answer (in markdown format):
            """
            chat_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
            )
            assistant_reply = chat_response.choices[0].message.content
            assistant_reply_safe = assistant_reply.replace("$", "\\$")
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply_safe})

# Scrollable chat history container
st.subheader("Chat History")
with st.container():
    st.markdown('<div class="chat-history" id="chat-history">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        role = "User" if message["role"] == "user" else "Assistant"
        with st.chat_message(role.lower()):
            st.markdown(message["content"])
    st.markdown('</div>', unsafe_allow_html=True)

# Input area for user queries with callback for submission
st.subheader("Ask a question about financial performances")
st.text_input(
    "Enter your question:",
    placeholder="Type your question here...",
    key="input_box",
    on_change=submit_query,
)
st.markdown('<div id="bottom"></div>', unsafe_allow_html=True)

# always focus on the latest question
st.markdown(
    """
    <script>
        var chatHistoryDiv = document.getElementById('chat-history');
        var bottomDiv = document.getElementById('bottom');
        if (chatHistoryDiv && bottomDiv) {
            bottomDiv.scrollIntoView({behavior: 'smooth'});
        }
    </script>
    """,
    unsafe_allow_html=True,
)

# Create a bottom container for the spinner
if "spinner_placeholder" not in st.session_state:
    st.session_state.spinner_placeholder = st.empty()
