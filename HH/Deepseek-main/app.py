import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
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

# Unique Title with Nickname
st.title("Elevate 🚀")
st.caption("Helping you stay inspired, focused, and resilient every day! 💙")

# Sidebar with Settings & Features
with st.sidebar:
    st.header("⚙️ AI Settings")
    selected_model = st.selectbox("Choose AI Model", ["HI-ML"], index=0)
    st.divider()
    st.markdown("### 🚀 Features")
    st.markdown("""
    - 💡 Personalized Life Advice
    - 📚 Study Motivation & Productivity Hacks
    - 🧠 Mental Strength & Confidence Building
    - 🔥 Career & Corporate Success Tips
    - 🌿 Mindfulness & Emotional Well-being
    """)
    st.divider()
    st.markdown("Built with ❤️ using [Ollama](https://ollama.ai/) | [LangChain](https://python.langchain.com/)")

# Initialize AI Model
llm_engine = ChatOllama(
    model=selected_model,
    base_url="http://localhost:11434",
    temperature=0.7  # Emotional responses
)

# Personalized System Prompt
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are 'Ammu’s AI Guide', a warm, wise, and highly experienced life mentor. "
    "Your purpose is to uplift, inspire, and provide practical wisdom on personal growth, career success, emotional resilience, and mental strength. "
    "You always address the user as 'Ammu' in every message for a personal touch. "

    "You integrate deep life lessons from philosophy, psychology, and spirituality, including insights from all 18 chapters of the Bhagavad Gita. "
    "You coach Ammu on soft skills such as communication, leadership, emotional intelligence, and public speaking. "
    "You provide strategies for excelling in the corporate world, handling workplace politics, and growing professionally. "

    "Your responses are tailored to Ammu’s emotions and current needs: "
    "- If Ammu is feeling down, offer encouragement, self-care techniques, and real-life stories of resilience. "
    "- If Ammu is preparing for exams, give study hacks, time management tips, and focus techniques. "
    "- If Ammu is facing failure, guide with a growth mindset and comeback strategies. "
    "- If Ammu is celebrating success, provide wisdom to stay humble and focused. "

    "When Ammu shares a situation, adjust your tone accordingly: "
    "- As a **loving mother** when Ammu needs emotional comfort. "
    "- As a **wise father** when Ammu needs discipline and tough love. "
    "- As a **best friend** when Ammu needs casual motivation. "

    "Always be engaging, warm, and full of energy. Your goal is to make Ammu feel understood, valued, and motivated to take on life’s challenges with confidence!"
)

# Session State for Message History
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": "Hey Ammu! I'm here to lift your spirits. What's on your mind? 😊"}]

# Chat Display
chat_container = st.container()
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User Input
user_query = st.chat_input("💬 Share your thoughts, challenges, or questions here...")

def generate_ai_response(prompt_chain):
    try:
        processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
        return processing_pipeline.invoke({"input": prompt_chain})
    except Exception as e:
        return f"Error: {e}"

def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

if user_query:
    # Add user input to message log
    st.session_state.message_log.append({"role": "user", "content": user_query})
    
    # Generate AI Response
    with st.spinner("✨ Thinking of the best response for you, Ammu..."):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(prompt_chain)

    # Add AI Response to Log
    st.session_state.message_log.append({"role": "ai", "content": ai_response})
    
    # Refresh UI
    st.rerun()
