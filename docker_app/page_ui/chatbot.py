import streamlit as st
import pandas as pd
from utils.s3_operations import save_to_s3

def render_chatbot(claude_chatbot):
    st.title("🤖 Claude Chatbot Assistant")
    st.write("""
    Welcome to your AI assistant for prompt engineering! Select a mode and start chatting.
    """)
    
    # Display pricing information
    with st.expander("💰 Pricing Information"):
        st.write("Set at 400 Input Tokens and 800 Output Tokens. Temperature is 0.3. Demo is running Claude 2.0, Claude 3 Sonnett is recommended model.")

        st.subheader("Claude Pricing")
        claude_pricing = pd.DataFrame({
            'Model': ['Claude 3 Sonnet', 'Claude 2.0'],
            'Price per 400 Token Input': ['$0.0012', '$0.0032'],
            'Price per 800 Token Output': ['$0.012', '$0.0192'],
            'Total per Input and Output Combined': ['$0.0132', '$0.0224']
        })
        st.table(claude_pricing)
    # Initialize conversation mode if not present
    if 'conversation_mode' not in st.session_state:
        st.session_state.conversation_mode = None

    # Dropdown for selecting conversation mode
    mode_options = [
        "Select a mode",
        "Improve Prompt",
        "Generate Prompt Ideas",
        "Ask Questions about Stability.ai SDXL 1.0/Amazon Titan G1"
    ]
    selected_mode = st.selectbox("Choose what you'd like to do:", mode_options)

    # Set conversation mode based on selection
    if selected_mode != "Select a mode":
        if selected_mode == "Improve Prompt":
            st.session_state.conversation_mode = "improve_prompt"
        elif selected_mode == "Generate Prompt Ideas":
            st.session_state.conversation_mode = "generate_idea"
        else:
            st.session_state.conversation_mode = "answer_questions"

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            role = "You" if message["role"] == "user" else "AI"
            bg_color = "#4a4a4a" if message["role"] == "user" else "#1e88e5"
            st.markdown(f"<div style='background-color: {bg_color}; color: #ffffff; padding: 10px; border-radius: 5px; margin-bottom: 10px;'><strong>{role}:</strong> {message['content']}</div>", unsafe_allow_html=True)

    # User input
    user_input = st.text_input("Your message:", key="user_input")

    col1, col2 = st.columns([3, 1])
    with col1:
        # Send button
        if st.button("Send", type="primary") and user_input:
            if st.session_state.conversation_mode is None:
                st.warning("Please select a mode before sending a message.")
            else:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                bot_response = claude_chatbot.get_chatbot_response(user_input, st.session_state.chat_history, st.session_state.conversation_mode)
                st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
                save_to_s3(st.session_state.chat_history, 'chat_history')
                st.rerun()

    with col2:
        # New Conversation button
        if st.button("New Conversation"):
            st.session_state.chat_history = []
            st.session_state.conversation_mode = None
            save_to_s3(st.session_state.chat_history, 'chat_history')
            st.rerun()

    # Display mode-specific instructions
    if st.session_state.conversation_mode == "improve_prompt":
        st.info("💡 Tip: Start by sharing your initial prompt, and I'll ask questions to help improve it step by step.")
    elif st.session_state.conversation_mode == "generate_idea":
        st.info("💡 Tip: Tell me about the company or theme you want to create a prompt for, and I'll generate ideas as a marketing expert.")
    elif st.session_state.conversation_mode == "answer_questions":
        st.info("💡 Tip: Ask me anything about Stability.ai SDXL 1.0 Image Generator or Amazon Titan Image Generator G1, including features, costs, and settings.")