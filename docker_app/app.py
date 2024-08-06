import streamlit as st
import boto3
from PIL import Image
import io
import base64
import numpy as np
from datetime import datetime
import time
import pandas as pd
import pickle

# Import custom modules and functions
from utils.auth import Auth
from config_file import Config
from models.stability import StabilityModel
from models.titan import TitanModel
from models.claude_chatbot import ClaudeChatbot
from models.claude_prompt_checker import ClaudePromptChecker
from models.chat_image_editor import ChatImageEditor
from page_ui.home import render_home
from page_ui.stability import render_stability
from page_ui.titan import render_titan
from page_ui.prompt_engineering import render_prompt_engineering
from page_ui.chatbot import render_chatbot
from page_ui.chat_image_editor import render_chat_image_editor
from utils.s3_operations import save_to_s3, load_from_s3, delete_from_s3

# Set up initial session state
def initialize_session_state():
    # Load or initialize various session states
    if 'stability_sessions' not in st.session_state:
        st.session_state.stability_sessions = load_from_s3('stability_sessions') or {}
    if 'titan_sessions' not in st.session_state:
        st.session_state.titan_sessions = load_from_s3('titan_sessions') or {}
    if 'current_session' not in st.session_state:
        st.session_state.current_session = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = load_from_s3('chat_history') or []
    if 'logged_out' not in st.session_state:
        st.session_state.logged_out = False
    if 'selected_image_index' not in st.session_state:
        st.session_state.selected_image_index = None
    if 'show_all_sessions' not in st.session_state:
        st.session_state.show_all_sessions = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"

def main():
    # Set up the Streamlit page
    st.set_page_config(page_title="AI Image Generator", layout="centered")
    
    # Initialize session state
    initialize_session_state()
    
    # Set up authentication
    secrets_manager_id = Config.SECRETS_MANAGER_ID
    authenticator = Auth.get_authenticator(secrets_manager_id)
    
    # Handle logout
    if 'logout_requested' not in st.session_state:
        st.session_state.logout_requested = False

    if st.session_state.logout_requested:
        st.session_state.clear()
        st.session_state.logout_requested = False
        st.rerun()
    
    # Perform login
    is_logged_in = authenticator.login()
    if not is_logged_in:
        st.stop()
        
    # Reset to home page on login
    if 'just_logged_in' not in st.session_state:
        st.session_state.just_logged_in = True
        st.session_state.current_page = "Home"
        st.rerun()

    if st.session_state.just_logged_in:
        st.session_state.just_logged_in = False
        
    # Logout function
    def logout():
        authenticator.logout()
        st.session_state.logout_requested = True
        st.session_state.current_page = "Home"  # Reset to home page on logout

    # Initialize AWS clients and models
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    s3_client = boto3.client('s3')

    stability_model = StabilityModel(client, s3_client, Config.S3_BUCKET_NAME)
    titan_model = TitanModel(client, s3_client, Config.S3_BUCKET_NAME)
    claude_chatbot = ClaudeChatbot(client, s3_client, Config.S3_BUCKET_NAME)
    claude_prompt_checker = ClaudePromptChecker(client, s3_client, Config.S3_BUCKET_NAME)
    chat_image_editor = ChatImageEditor(client, s3_client, Config.S3_BUCKET_NAME)
    
    # Set up the sidebar
    with st.sidebar:
        st.text(f"Welcome,\n{authenticator.get_username()}")
        st.button("Logout", "logout_btn", on_click=logout)
        st.markdown("---")
        page = st.radio("Navigation", ["Home", "Stability.ai SDXL 1.0 Image Generator", "Amazon Titan Image Generator G1", "Amazon Titan Image Chat Editor", "Prompt Engineering: Best Practices", "Claude Chatbot Assistant"])        
        # Update current_page when navigation changes
        if page != st.session_state.current_page:
            st.session_state.current_page = page
            st.session_state.current_session = None  # Reset current session when changing pages
            st.rerun()

    # Render the appropriate page based on the current selection
    if st.session_state.current_page == "Home":
        render_home()
    elif st.session_state.current_page == "Stability.ai SDXL 1.0 Image Generator":
        render_stability(stability_model)
    elif st.session_state.current_page == "Amazon Titan Image Generator G1":
        render_titan(titan_model)
    elif st.session_state.current_page == "Amazon Titan Image Chat Editor":
        render_chat_image_editor(chat_image_editor)
    elif st.session_state.current_page == "Prompt Engineering: Best Practices":
        render_prompt_engineering(claude_prompt_checker)
    elif st.session_state.current_page == "Claude Chatbot Assistant":
        render_chatbot(claude_chatbot)

if __name__ == "__main__":
    main()