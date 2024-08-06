import streamlit as st
from PIL import Image
import io
import numpy as np
from datetime import datetime
import time
import boto3
from config_file import Config
from utils.s3_operations import save_image_to_s3, delete_image_from_s3, save_to_s3, load_from_s3, delete_from_s3

# Function to display an image stored in S3
def display_s3_image(image_key):
    s3 = boto3.client('s3')
    img_data = s3.get_object(Bucket=Config.S3_BUCKET_NAME, Key=image_key)['Body'].read()
    img = Image.open(io.BytesIO(img_data))
    st.image(img, use_column_width=True)

# Main function to render the chat image editor interface
def render_chat_image_editor(chat_image_editor):
    st.title("Amazon Titan Image Chat Editor")
    
    # Load or initialize chat image editor sessions
    if 'chat_image_editor_sessions' not in st.session_state:
        st.session_state.chat_image_editor_sessions = load_from_s3('chat_image_editor_sessions') or {}

    sessions = st.session_state.chat_image_editor_sessions
    
    # Handle session management
    session = handle_model_session("chat_image_editor", sessions, chat_image_editor)
    if not session:
        return

    # Display chat history
    for i, entry in enumerate(session['chat_history']):
        if entry['type'] == 'user':
            st.text_area("You:", entry['content'], height=50, disabled=True, key=f"user_{i}")
        elif entry['type'] == 'assistant':
            st.text_area("Assistant:", entry['content'], height=50, disabled=True, key=f"assistant_{i}")
        elif entry['type'] == 'image':
            display_s3_image(entry['content'])
            # Provide download button for the image
            s3 = boto3.client('s3')
            img_data = s3.get_object(Bucket=Config.S3_BUCKET_NAME, Key=entry['content'])['Body'].read()
            st.download_button(
                label="Download Image",
                data=img_data,
                file_name=f"image_{i}.png",
                mime="image/png",
                key=f"download_{i}"
            )
    
    # Determine if there's a current image to edit
    current_image_entry = next((entry for entry in reversed(session['chat_history']) if entry['type'] == 'image'), None)
    
    if current_image_entry is None:
        # If no current image, provide interface to generate a new image
        user_input = st.text_input("Enter your prompt to generate an image:")
        if st.button("Generate Image"):
            if user_input:
                session['chat_history'].append({'type': 'user', 'content': user_input})
                try:
                    with st.spinner("Generating image..."):
                        images = chat_image_editor.generate_image(prompt=user_input)
                        if images and len(images) > 0:
                            image = images[0]  # Take the first image
                            image_key = save_image_to_s3(image, f"chat_image_editor_sessions/{st.session_state.current_session}/images")
                            session['chat_history'].append({'type': 'image', 'content': image_key})
                        else:
                            session['chat_history'].append({'type': 'assistant', 'content': "Sorry, I couldn't generate the image. Please try again."})
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    session['chat_history'].append({'type': 'assistant', 'content': f"An error occurred: {str(e)}"})
                save_to_s3(st.session_state.chat_image_editor_sessions, "chat_image_editor_sessions")
                st.rerun()
    else:
        # If there's a current image, provide interface for editing
        edit_mode = st.radio("Edit Mode", ["Inpainting", "Outpainting"], help="Choose between inpainting (edit within image) or outpainting (extend image).")
        mask_prompt = st.text_input("Mask Prompt", help="Describe the area you want to edit or extend.")
        edit_prompt = st.text_input("Edit Prompt", help="Describe what you want to add or change in the selected area.")
        
        if st.button("Edit Image"):
            if edit_prompt and mask_prompt:
                session['chat_history'].append({'type': 'user', 'content': f"Mode: {edit_mode}\nMask: {mask_prompt}\nEdit: {edit_prompt}"})
                try:
                    with st.spinner("Editing image..."):
                        s3 = boto3.client('s3')
                        img_data = s3.get_object(Bucket=Config.S3_BUCKET_NAME, Key=current_image_entry['content'])['Body'].read()
                        current_image = Image.open(io.BytesIO(img_data))
                        images = chat_image_editor.edit_image(
                            prompt=edit_prompt,
                            init_image=current_image,
                            mask_prompt=mask_prompt,
                            outpainting=(edit_mode == "Outpainting")
                        )
                        if images and len(images) > 0:
                            image = images[0]  # Take the first image
                            image_key = save_image_to_s3(image, f"chat_image_editor_sessions/{st.session_state.current_session}/images")
                            session['chat_history'].append({'type': 'image', 'content': image_key})
                        else:
                            session['chat_history'].append({'type': 'assistant', 'content': "Sorry, I couldn't edit the image. Please try again."})
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    session['chat_history'].append({'type': 'assistant', 'content': f"An error occurred: {str(e)}"})
                save_to_s3(st.session_state.chat_image_editor_sessions, "chat_image_editor_sessions")
                st.rerun()
                
    # Button to clear chat history
    if st.button("Clear Chat"):
        session['chat_history'] = []
        session['current_image'] = None
        save_to_s3(st.session_state.chat_image_editor_sessions, "chat_image_editor_sessions")
        st.rerun()

# Function to handle session management
def handle_model_session(model, sessions, model_instance):
    with st.expander("Session Management"):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("All Sessions"):
                st.session_state.show_all_sessions = True
                st.rerun()
        with col2:
            if st.button("Delete Current Session"):
                if st.session_state.current_session:
                    del sessions[st.session_state.current_session]
                    delete_from_s3(f"{model}_sessions/{st.session_state.current_session}")
                    st.session_state.current_session = None
                    save_to_s3(sessions, f"{model}_sessions")
                    st.success(f"Session deleted.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("No current session to delete.")
        # Create a list of session names, sorted by timestamp
        session_names = list(sessions.keys())
        session_names.sort(key=lambda x: sessions[x].get('timestamp', ''), reverse=True)
        session_names.append("New Session")

        # Format function for session names
        def format_func(session_name):
            if session_name == "New Session":
                return f"🆕 New Session"
            else:
                return f"📁 {session_name}"

        # Dropdown to select a session
        selected_session = st.selectbox(
            "Select Session",
            session_names,
            format_func=format_func,
            key=f"{model}_session_select",
            index=session_names.index(st.session_state.current_session) if st.session_state.current_session in session_names else 0
        )

        # Handle new session creation
        if selected_session == "New Session":
            new_session_name = st.text_input("Enter new session name")
            if st.button("Create Session") and new_session_name:
                if new_session_name in sessions:
                    st.error(f"Session '{new_session_name}' already exists. Please choose a different name.")
                else:
                    sessions[new_session_name] = {
                        'chat_history': [],
                        'current_image': None,
                        'timestamp': datetime.now().isoformat()
                    }
                    st.session_state.current_session = new_session_name
                    st.session_state.current_model = model
                    save_to_s3(sessions, f"{model}_sessions")
                    st.success(f"New session '{new_session_name}' created!")
                    time.sleep(1)
                    st.rerun()
        elif selected_session != st.session_state.current_session:
            st.session_state.current_session = selected_session
            st.session_state.current_model = model
            st.rerun()

    # Display all sessions if requested
    if getattr(st.session_state, 'show_all_sessions', False):
        display_all_sessions(model, sessions)
        return None

    # Ensure a session is selected
    if st.session_state.current_session not in sessions:
        st.warning("Please select or create a session to continue.")
        return None

    return sessions[st.session_state.current_session]

# Function to display all sessions
def display_all_sessions(model, sessions):
    st.subheader(f"All {model.capitalize()} Sessions")
    if not sessions:
        st.write("No sessions found.")
    else:
        for session_name, session_data in sorted(sessions.items(), key=lambda x: x[1].get('timestamp', ''), reverse=True):
            timestamp = datetime.fromisoformat(session_data.get('timestamp', ''))
            formatted_time = timestamp.strftime("%m/%d/%Y, %H:%M UTC")
            
            st.markdown(f"""
            <div style='background-color: #4a4a4a; color: #ffffff; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                <strong>{session_name}</strong><br>
                Last modified: {formatted_time}
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Open", key=f"open_{model}_{session_name}"):
                    st.session_state.current_session = session_name
                    st.session_state.show_all_sessions = False
                    st.rerun()
            with col2:
                if st.button("Delete", key=f"delete_{model}_{session_name}"):
                    del sessions[session_name]
                    delete_from_s3(f"{model}_sessions/{session_name}")
                    save_to_s3(sessions, f"{model}_sessions")
                    st.success(f"Session '{session_name}' deleted.")
                    time.sleep(1)
                    st.rerun()

    if st.button("Back to Current Session"):
        st.session_state.show_all_sessions = False
        st.rerun()