import streamlit as st
import requests
import json

# Configuration
# API_URL = "http://127.0.0.1:8000"  # Local FastAPI URL
API_URL = "https://personality-backend-jfb1.onrender.com" # renderAPI URL

st.set_page_config(page_title="Personality Engine", layout="wide")

st.title("🧠 Modular Personality Engine")
st.markdown("Architecture: **FastAPI (Backend)** + **Streamlit (Frontend)**")

# --- Initialize Session State ---
if 'memory' not in st.session_state:
    st.session_state['memory'] = None

# --- Sidebar: Ingestion ---
with st.sidebar:
    st.header("1. Ingest Data")
    default_data = """User: I hate Mondays, they make me so anxious.
User: My cat Luna threw up today, I'm worried.
User: I wish I could just play Elden Ring all day.
User: Coffee makes me jittery but I drink it anyway.
User: I'm trying to learn Python but it's hard."""

    chat_input = st.text_area("User Chat History", value=default_data, height=256)

    if st.button("Analyze & Build Memory"):
        with st.spinner("Calling API /extract-memory..."):
            try:
                pay_load = {"messages": chat_input}
                
                response = requests.post(f"{API_URL}/extract-memory", json=pay_load)

                if response.status_code == 200:
                    st.session_state['memory'] = response.json()
                    st.success("Memory Profile Built!")
                else:
                    st.error(f"Error: {response.text}")

            except Exception as e:
                st.error(f"Connection Failed: {e}")

# --- Main Interface ---
col1, col2 = st.columns([1, 1])

# Left Column: The "Brain" (Memory View)
with col1:
    st.subheader("Memory State (JSON)")
    if st.session_state['memory']:
        st.json(st.session_state['memory'])
    else:
        st.info("No memory loaded. Please analyze chat logs first.")
        
# Right Column: The "Interaction" (Chat)
with col2:
    st.subheader("Personality Interface")

    persona = st.selectbox("Select Persona", ["Calm Mentor", "Witty Friend", "Therapist"])
    user_query = st.text_input("User Input", placeholder="e.g. I am feeling stressed.")

    if st.button("Generate Response"):
        if not st.session_state['memory']:
            st.warning("Please build memory first.")
        else:
            with st.spinner("Calling API /chat..."):
                pay_load = {
                    "user_query": user_query,
                    "memory_context": st.session_state['memory'],
                    "persona": persona                  
                }

                # Call endpoint
                response = requests.post(f"{API_URL}/chat", json=pay_load)

                if response.status_code == 200:
                    data = response.json()

                    # COMPARISON UI
                    st.markdown("### 🆚 Response Comparison")
                    
                    st.markdown("**❌ Before (Standard AI):**")
                    st.info(data['original_response'])
                    
                    st.markdown(f"**✅ After ({persona}):**")
                    st.success(data['personalized_response'])
                
                else:
                    st.error(f"API Error: {response.text}")