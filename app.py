import streamlit as st
import google.generativeai as genai
import os
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Exam Cram Buddy",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Agent Exam Cram")
st.caption("Your strict but helpful AI University Tutor")

# --- SIDEBAR & API KEY ---
with st.sidebar:
    st.header("Settings")
    # Try to get key from Azure Environment first, otherwise ask user
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        api_key = st.text_input("Enter Gemini API Key", type="password")
    
    st.markdown("---")
    if st.button("Reset Session"):
        st.session_state.messages = []
        st.session_state.chat_session = None
        st.experimental_rerun()

# --- SETUP GEMINI ---
if not api_key:
    st.warning("Please enter your Google API Key in the sidebar to start.")
    st.stop()

try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error configuring API: {e}")
    st.stop()

# --- TOOLS DEFINITION ---
def lookup_textbook(topic: str):
    """Simulates verifying facts from a textbook."""
    return f"Textbook Definition: {topic} is a fundamental concept in the study material."

def give_hint(concept: str):
    """Provides a hint without giving the answer."""
    return f"Hint: Think about how {concept} relates to the core principles."

# --- INITIALIZE SESSION STATE ---
# We need to store history in memory so it doesn't vanish when you click buttons
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state or st.session_state.chat_session is None:
    # Initialize the Tutor Agent
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        tools=[lookup_textbook, give_hint]
    )
    st.session_state.chat_session = model.start_chat(enable_automatic_function_calling=True)
    
    # Send the System Instruction silently
    system_prompt = """
    You are 'Exam Cram Buddy', a strict university tutor.
    1. Ask the user what subject they are studying.
    2. When they reply, IMMEDIATELY ask a hard quiz question.
    3. If they ask for help, use `give_hint`.
    4. Verify answers with `lookup_textbook`.
    """
    response = st.session_state.chat_session.send_message(system_prompt)
    
    # Add initial greeting
    st.session_state.messages.append({"role": "model", "content": response.text})

# --- DISPLAY CHAT HISTORY ---
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg["content"])

# --- HANDLE USER INPUT ---
if prompt := st.chat_input("Type your answer here..."):
    # 1. Display User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Check for "Finish" command (Multi-Agent Handoff)
    if prompt.lower() in ["exit", "quit", "finish"]:
        with st.chat_message("assistant"):
            with st.spinner("Generating Report Card..."):
                # Initialize Evaluator Agent
                grader_model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Create Transcript
                transcript = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                
                grader_prompt = f"""
                You are the Exam Board Evaluator. Analyze this study session.
                1. Subject studied.
                2. Correct/Incorrect answers.
                3. Final Grade (A-F).
                
                TRANSCRIPT:
                {transcript}
                """
                report_card = grader_model.generate_content(grader_prompt).text
                st.markdown("### 🎓 Final Report Card")
                st.markdown(report_card)
                
                # Append to history so it stays on screen
                st.session_state.messages.append({"role": "model", "content": report_card})
                
    else:
        # 3. Standard Tutor Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.chat_session.send_message(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "model", "content": response.text})
                except Exception as e:
                    st.error(f"Error: {e}")