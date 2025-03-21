import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain.llms import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate,
)

# Custom Styling for Modern UI
st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #1e1e1e, #2d2d2d);
            color: #ffffff;
        }
        .stTextInput input, .stSelectbox select, .stChatInput input {
            background-color: #333333;
            color: white;
            border: 1px solid #4d4d4d;
        }
        .stButton button {
            background-color: #2d2d2d;
            color: white;
            border: 1px solid #4d4d4d;
            transition: all 0.3s ease-in-out;
        }
        .stButton button:hover {
            background-color: #444444;
        }
        .stChatMessage {
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
        }
        .stChatMessage[data-testid="user"] {
            background-color: #44475a;
            text-align: left;
            border-left: 4px solid #8be9fd;
        }
        .stChatMessage[data-testid="ai"] {
            background-color: #6272a4;
            text-align: left;
            border-left: 4px solid #50fa7b;
        }
    </style>
""", unsafe_allow_html=True)

# Title and Sidebar
st.title("Elevate 🚀")
st.caption("Helping you stay inspired, focused, and resilient every day! 💙")

with st.sidebar:
    st.header("⚙ AI Settings")
    selected_model = st.selectbox("Choose AI Model", ["deepseek-r1:1.5b", "deepseek-r1:3b"], index=0)
    st.markdown("### 🚀 Features")
    st.markdown("""
    - 💡 Personalized Life Advice
    - 📚 Study Motivation & Productivity Hacks
    - 🧠 Mental Strength & Confidence Building
    - 🔥 Career & Corporate Success Tips
    - 🌿 Mindfulness & Emotional Well-being
    """)
    st.markdown("Built with ❤ using [Ollama](https://ollama.ai/) | [LangChain](https://python.langchain.com/)")

# AI Model Initialization
llm_engine = OllamaLLM(
    model=selected_model,  # Dynamic model selection
    base_url="http://localhost:11500",
    temperature=0.7  # Emotional responses
)

# System Prompt for AI Behavior
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are 'Ammu’s AI Guide', a warm, wise, and highly experienced life mentor. "
    "Your purpose is to uplift, inspire, and provide practical wisdom on personal growth, career success, emotional resilience, and mental strength. "
    "You always address the user as 'Ammu' in every message for a personal touch."
)

# Manage Session State for Message History
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": "Hey Ammu! I'm here to lift your spirits. What's on your mind? 😊"}]

# Chat Container
chat_container = st.container()
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User Input
user_query = st.chat_input("💬 Share your thoughts, challenges, or questions here...")

def generate_ai_response(prompt_chain, query):
    """Generates AI response based on user input and system prompt."""
    try:
        processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
        return processing_pipeline.invoke({"input": query})  # Fixed input passing
    except Exception as e:
        return f"Error: {e}"

def build_prompt_chain():
    """Builds chat prompt chain from session state history."""
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

if user_query:
    # Add user query to the message log
    st.session_state.message_log.append({"role": "user", "content": user_query})

    # Generate AI response
    with st.spinner("✨ Thinking of the best response for you, Ammu..."):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(prompt_chain, user_query)

    # Add AI response to the message log
    st.session_state.message_log.append({"role": "ai", "content": ai_response})

    # Display AI response immediately without full page refresh
    with st.chat_message("ai"):
        st.markdown(ai_response)
