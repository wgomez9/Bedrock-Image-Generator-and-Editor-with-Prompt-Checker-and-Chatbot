import streamlit as st
from PIL import Image
import random
import io
import numpy as np
from streamlit_drawable_canvas import st_canvas
from datetime import datetime
import time
import boto3
from config_file import Config
from utils.s3_operations import save_image_to_s3, delete_image_from_s3, save_to_s3, load_from_s3, delete_from_s3
import cv2

# Helper function to display an image stored in S3
# 
# This function retrieves an image from the S3 bucket and displays it in the Streamlit app.
# It uses the boto3 client to fetch the image data, converts it to a PIL Image object,
# and then uses Streamlit's image display function to show it.
#
# Parameters:
# - image_key: The S3 key of the image to be displayed

def display_s3_image(image_key):
    s3 = boto3.client('s3')
    img_data = s3.get_object(Bucket=Config.S3_BUCKET_NAME, Key=image_key)['Body'].read()
    img = Image.open(io.BytesIO(img_data))
    st.image(img, use_column_width=True)

# Function to display multiple images with selection and removal options
#
# This function creates a grid display of images stored in S3, allowing users to select,
# download, or remove images. It handles the layout, selection logic, and updates the
# session state based on user interactions.
#
# Parameters:
# - image_keys: List of S3 keys for the images to be displayed
# - key_prefix: A prefix used to create unique keys for Streamlit widgets
# - allow_select: Boolean to enable/disable image selection
# - allow_remove: Boolean to enable/disable image removal
#
# Returns:
# - selected_image_key: The S3 key of the selected image (if any)
# - selected_index: The index of the selected image in the image_keys lists

def display_images(image_keys, key_prefix, allow_select=True, allow_remove=True):
    if not image_keys:
        return None, None

    num_cols = 3
    num_rows = (len(image_keys) + num_cols - 1) // num_cols

    selected_image_key = None
    selected_index = None

    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col in range(num_cols):
            idx = row * num_cols + col
            if idx < len(image_keys):
                image_key = image_keys[idx]
                with cols[col]:
                    display_s3_image(image_key)
                    col1, col2, col3 = st.columns([1, 1, 2])
                    with col1:
                        if allow_select:
                            session_specific_key = f'{st.session_state.current_session}_{key_prefix}_selected_index'
                            is_selected = st.session_state.get(session_specific_key) == idx
                            button_label = "✓" if is_selected else "☐"
                            if st.button(button_label, key=f"{key_prefix}_select_{idx}"):
                                st.session_state[session_specific_key] = idx
                                selected_image_key = image_key
                                selected_index = idx
                                st.rerun()
                    with col2:
                        s3 = boto3.client('s3')
                        img_data = s3.get_object(Bucket=Config.S3_BUCKET_NAME, Key=image_key)['Body'].read()
                        st.download_button("⬇️", img_data, f"image_{idx}.png", "image/png")
                    with col3:
                        if allow_remove and st.button("🗑️", key=f"{key_prefix}_remove_{idx}"):
                            session = st.session_state[f'{st.session_state.current_model}_sessions'][st.session_state.current_session]
                            session[f'{key_prefix}_images'].remove(image_key)
                            delete_image_from_s3(image_key)
                            
                            # Remove the corresponding uploaded file
                            if 'uploaded_files' in st.session_state:
                                uploaded_files = st.session_state.uploaded_files
                                for file in uploaded_files:
                                    if file.name == image_key.split('/')[-1]:
                                        uploaded_files.remove(file)
                                        break
                                st.session_state.uploaded_files = uploaded_files
                            
                            # Clear selection if the deleted image was selected
                            if st.session_state.get(session_specific_key) == idx:
                                st.session_state[session_specific_key] = None
                                session[f'selected_{key_prefix}_image'] = None
                                session[f'selected_{key_prefix}_index'] = None
                            save_to_s3(st.session_state[f'{st.session_state.current_model}_sessions'], f"{st.session_state.current_model}_sessions")
                            st.rerun()
    
    session_specific_key = f'{st.session_state.current_session}_{key_prefix}_selected_index'
    if st.session_state.get(session_specific_key) is not None:
        selected_index = st.session_state[session_specific_key]
        if selected_index < len(image_keys):
            selected_image_key = image_keys[selected_index]
        else:
            st.session_state[session_specific_key] = None

    return selected_image_key, selected_index

# Main function to render the Stability.ai interface
#
# This function sets up the main interface for the Stability.ai SDXL 1.0 Image Generator.
# It manages the overall flow of the application, handling session state and directing
# the user through the steps of base image generation, variation, and editing.
#
# Parameters:
# - stability_model: An instance of the StabilityModel class for image generation

def render_stability(stability_model):
    st.title("Stability.ai SDXL 1.0 Image Generator")
    
    sessions = st.session_state.stability_sessions
    
    session = handle_model_session("stability", sessions, stability_model)
    if not session:
        return

    # Render appropriate step based on session state
    if session['step'] == 'base':
        display_base_step(session, stability_model)
    elif session['step'] == 'variation':
        display_variation_step(session, stability_model)
    elif session['step'] == 'editing':
        display_editing_step(session, stability_model)

# Function to handle the base image generation step
#
# This function creates the interface for generating base images using the Stability.ai model.
# It provides controls for entering prompts, selecting image settings, and initiating
# the image generation process. It also handles image uploads and displays generated images.
#
# Parameters:
# - session: The current user session containing state information
# - stability_model: An instance of the StabilityModel class for image generation
def display_base_step(session, stability_model):
    st.header("Step 1: Base Image Generation")

    # Create a unique key prefix for this session and step
    key_prefix = f"{st.session_state.current_session}_base_"
    
    # Text input for prompt and negative prompt
    prompt = st.text_area("Text Prompt", key=key_prefix+"base_prompt", max_chars=2000, 
                           help="Describe the image you want to generate. Be specific and detailed.")
    negative_prompt = st.text_input("Negative Text Prompt (optional)", key=key_prefix+"negative_prompt", max_chars=2000,
                                    help="Describe what not to include in the image. This helps refine the output.")

    # Image generation settings
    col1, col2, col3 = st.columns(3)
    with col1:
        # Resolution selection
        sizes = [
            "1024x1024 (1:1)", "512x512 (1:1)",
            "1152x896 (Landscape)", "1216x832 (Landscape)", "1344x768 (Landscape)", "1536x640 (Landscape)",
            "896x1152 (Portrait)", "832x1216 (Portrait)", "768x1344 (Portrait)", "640x1536 (Portrait)"
        ]
        size = st.selectbox("Resolution", sizes, index=0, key=key_prefix+"resolution",
                            help="Select the pixel width and height. Higher pixel count =  higher level of detail. Default: 1024x1024 (1:1)")
        width, height = map(int, size.split()[0].split('x'))
    with col2:
        # Style preset selection
        style_preset = st.selectbox("Style Preset", ["None",
            "photographic", "analog-film", "anime", "cinematic", "comic-book", "digital-art",
            "enhance", "fantasy-art", "isometric", "line-art", "low-poly", "modeling-compound",
            "neon-punk", "origami", "3d-model", "pixel-art", "tile-texture"
        ], key=key_prefix+"base_style_preset", help="Guides image model towards a particular style. This influences the overall look. Default: None")
        style_preset = None if style_preset == "None" else style_preset

    with col3:
        # Seed selection
        seed = st.number_input("Seed", value=0, min_value=0, max_value=4294967295, key=key_prefix+"seed",
                               help="Set a seed for reproducible results. Use 0 for random seed. Default: 0")
        if seed == 0:
            seed = random.randint(0, 4294967295)

    # Advanced settings
    with st.expander("Advanced Settings"):
        col1, col2 = st.columns(2)
        with col1:
            sampler = st.selectbox("Sampler", [
                "DDIM", "DDPM", "K_DPMPP_2M", "K_DPMPP_2S_ANCESTRAL", "K_DPM_2",
                "K_DPM_2_ANCESTRAL", "K_EULER", "K_EULER_ANCESTRAL", "K_HEUN", "K_LMS"
            ], key=key_prefix+"sampler", help="A sampler is a method of generating data in a specific way. Different samplers can produce noticeable different results. The type of sampler chosen affects how the data transformation is performed, from a noisy initial state to a clear and detailed final image. Default: DDIM")
        with col2:
            clip_guidance_preset = st.selectbox("CLIP Guidance Preset", [
                "NONE", "FAST_BLUE", "FAST_GREEN", "SIMPLE", "SLOW", "SLOWER", "SLOWEST"
            ], key=key_prefix+"base_clip_guidance_preset", help="A technique that uses the CLIP neural network to guide the generation of images to be more in-line with your included prompt, which often results in improved coherency. Default: NONE")
        cfg_scale = st.slider("CFG Scale", 0, 35, 7, key=key_prefix+"cfg_scale",
                              help="Determines how much the final image portrays the prompt. Lower values = higher randomness. Default: 7")
        steps = st.slider("Steps", 10, 150, 70, key=key_prefix+"steps",
                          help="Determines how many times the image is sampled. More steps can result in a more accurate result with longer processing time. Default: 70")


    # Image upload functionality
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []

    uploaded_files = st.file_uploader("Upload images", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"{st.session_state.current_session}_base_uploader")
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file not in st.session_state.uploaded_files:
                image = Image.open(uploaded_file)
                width, height = image.size
                if f"{width}x{height}" in [size.split()[0] for size in sizes]:
                    image_key = save_image_to_s3(image, f"{st.session_state.current_model}_sessions/{st.session_state.current_session}/base_images")
                    if image_key not in session['base_images']:
                        session['base_images'].append(image_key)
                        save_to_s3(st.session_state[f'{st.session_state.current_model}_sessions'], f"{st.session_state.current_model}_sessions")
                    st.session_state.uploaded_files.append(uploaded_file)
                else:
                    st.warning(f"Uploaded image size ({width}x{height}) is not supported. Please upload images with supported sizes.")

    # Generate base image button
    if st.button("Generate Base Image", disabled=not prompt, help="Missing text prompt" if not prompt else ""):
        with st.spinner("Generating image..."):
            image = stability_model.invoke_text_to_image(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                style_preset=style_preset,
                seed=seed,
                clip_guidance_preset=clip_guidance_preset,
                cfg_scale=cfg_scale,
                steps=steps,
                sampler=sampler
            )
            if image:
                image_key = save_image_to_s3(image, f"stability_sessions/{st.session_state.current_session}/base_images")
                session['base_images'].append(image_key)
                save_to_s3(st.session_state.stability_sessions, "stability_sessions")

    # Display generated and uploaded images
    st.subheader("Generated and Uploaded Images")
    selected_image_key, selected_index = display_images(session['base_images'], "base", allow_remove=True)
    
    # Update the session with the currently selected image
    if selected_image_key:
        session['selected_base_image'] = selected_image_key
        session['selected_base_index'] = selected_index
    else:
        # Remove the selection if no image is selected (e.g., after deletion)
        session.pop('selected_base_image', None)
        session.pop('selected_base_index', None)
    
    save_to_s3(st.session_state.stability_sessions, "stability_sessions")

    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write("")
    with col2:
        button_disabled = 'selected_base_image' not in session
        button_type = "secondary" if button_disabled else "primary"
        
        if st.button("Next: Image Variation", key="next_to_variation", type=button_type, disabled=button_disabled):
            session['step'] = 'variation'
            save_to_s3(st.session_state.stability_sessions, "stability_sessions")
            st.rerun()
        
        if 'selected_base_image' in session:
            st.success("Image Selected")
        else:
            st.error("Please select an image before proceeding.")

# Function to handle the image variation step
#
# This function provides an interface for creating variations of a selected base image.
# It allows users to adjust parameters and generate new versions of their chosen image.
# The function also handles the display and selection of generated variations.
#
# Parameters:
# - session: The current user session containing state information
# - stability_model: An instance of the StabilityModel class for image generation
def display_variation_step(session, stability_model):
    st.header("Step 2: Image Variation")

    # Create a unique key prefix for this session and step
    key_prefix = f"{st.session_state.current_session}_variation_"

    col1, col2 = st.columns([1, 1])
    with col1:
        if 'selected_base_image' in session:
            display_s3_image(session['selected_base_image'])
    
    with col2:
        prompt = st.text_input("Text Prompt (optional)", key=key_prefix+"prompt", max_chars=2000,
                               help="Describe how you want to modify the selected image.")
        negative_prompt = st.text_input("Negative Text Prompt (optional)", key=key_prefix+"negative_prompt", max_chars=2000,
                                        help="Describe what not to include in the image. This helps refine the output.")
        
        col1, col2 = st.columns(2)
        with col1:
            style_preset = st.selectbox("Style Preset", ["None",
                "photographic", "analog-film", "anime", "cinematic", "comic-book", "digital-art",
                "enhance", "fantasy-art", "isometric", "line-art", "low-poly", "modeling-compound",
                "neon-punk", "origami", "3d-model", "pixel-art", "tile-texture"
            ], key=key_prefix+"style_preset", help="Guides image model towards a particular style. This influences the overall look. Default: None")
            style_preset = None if style_preset == "None" else style_preset

        with col2:
            seed = st.number_input("Seed", value=0, min_value=0, max_value=4294967295, key=key_prefix+"seed",
                                   help="Set a seed for reproducible results. Use 0 for random seed. Default: 0")
            if seed == 0:
                seed = random.randint(0, 4294967295)
        image_strength = st.slider("Image Strength", 0.0, 1.0, 0.35, key=key_prefix+"image_strength",
                                   help="Controls how similar the variation is to the original. Higher values = more similar. Default: 0.35")
        
    with st.expander("Advanced Settings"):
        col1, col2 = st.columns(2)
        with col1:
            sampler = st.selectbox("Sampler", [
                "DDIM", "DDPM", "K_DPMPP_2M", "K_DPMPP_2S_ANCESTRAL", "K_DPM_2",
                "K_DPM_2_ANCESTRAL", "K_EULER", "K_EULER_ANCESTRAL", "K_HEUN", "K_LMS"
            ], key=key_prefix+"sampler", help="A sampler is a method of generating data in a specific way. Different samplers can produce noticeable different results. The type of sampler chosen affects how the data transformation is performed, from a noisy initial state to a clear and detailed final image. Default: DDIM")
        with col2:
            clip_guidance_preset = st.selectbox("CLIP Guidance Preset", [
                "NONE", "FAST_BLUE", "FAST_GREEN", "SIMPLE", "SLOW", "SLOWER", "SLOWEST"
            ], key=key_prefix+"base_clip_guidance_preset", help="A technique that uses the CLIP neural network to guide the generation of images to be more in-line with your included prompt, which often results in improved coherency. Default: NONE")
        cfg_scale = st.slider("CFG Scale", 0, 35, 7, key=key_prefix+"cfg_scale",
                              help="Determines how much the final image portrays the prompt. Lower values = higher randomness. Default: 7")
        steps = st.slider("Steps", 10, 150, 70, key=key_prefix+"steps",
                          help="Determines how many times the image is sampled. More steps can result in a more accurate result with longer processing time. Default: 70")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Variations", key="generate_variations"):
            with st.spinner("Generating variations..."):
                s3 = boto3.client('s3')
                img_data = s3.get_object(Bucket=Config.S3_BUCKET_NAME, Key=session['selected_base_image'])['Body'].read()
                init_image = Image.open(io.BytesIO(img_data))
                image = stability_model.invoke_image_variation(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    init_image=init_image,
                    image_strength=image_strength,
                    style_preset=style_preset,
                    clip_guidance_preset=clip_guidance_preset,
                    seed=seed,
                    cfg_scale=cfg_scale,
                    steps=steps,
                    sampler=sampler
                )
                if image:
                    image_key = save_image_to_s3(image, f"stability_sessions/{st.session_state.current_session}/variation_images")
                    session['variation_images'].append(image_key)
                    save_to_s3(st.session_state.stability_sessions, "stability_sessions")
            st.rerun()
    
    with col2:
        use_original = st.checkbox("Use Original Image", key="use_original_variation")

    # Initialize session state for selection
    if 'variation_selection' not in st.session_state:
        st.session_state.variation_selection = 'none'

    st.subheader("Generated Variations")
    selected_image_key, selected_index = display_images(session['variation_images'], "variation", allow_remove=True)

    # Handle mutual exclusivity
    if use_original:
        st.session_state.variation_selection = 'original'
    elif selected_image_key:
        st.session_state.variation_selection = 'variation'
    else:
        st.session_state.variation_selection = 'none'

    # Update the session based on the selection
    if st.session_state.variation_selection == 'original':
        selected_image_key = session.get('selected_base_image')
        selected_index = None
    elif st.session_state.variation_selection == 'variation':
        # Keep the selected variation
        pass
    else:
        selected_image_key = None
        selected_index = None

    # Update the session with the currently selected image
    if selected_image_key:
        session['selected_variation_image'] = selected_image_key
        session['selected_variation_index'] = selected_index
    else:
        session.pop('selected_variation_image', None)
        session.pop('selected_variation_index', None)
    
    save_to_s3(st.session_state.stability_sessions, "stability_sessions")
   
    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back: Base Image", key="back_to_base", type="primary"):
            session['step'] = 'base'
            save_to_s3(st.session_state.stability_sessions, "stability_sessions")
            st.rerun()
    with col2:
        button_disabled = not (selected_image_key or use_original)
        button_type = "secondary" if button_disabled else "primary"
        
        if st.button("Next: Image Editing", key="next_to_editing", type=button_type, disabled=button_disabled):
            session['editing_image'] = selected_image_key
            session['step'] = 'editing'
            save_to_s3(st.session_state.stability_sessions, "stability_sessions")
            st.rerun()
        
        if st.session_state.variation_selection == 'original':
            st.success("Original Image Selected")
        elif st.session_state.variation_selection == 'variation':
            st.success("Variation Selected")
        else:
            st.error("Please select an image or use the original before proceeding.")

# Constants to scale the image down
CANVAS_WIDTH = 512
# Function to handle the image editing step
#
# This function creates an interface for editing images using inpainting techniques.
# It provides a canvas for users to draw masks on the image and controls for adjusting
# editing parameters. The function processes the edits and displays the results.
#
# Parameters:
# - session: The current user session containing state information
# - stability_model: An instance of the StabilityModel class for image generation
def display_editing_step(session, stability_model):
    st.header("Step 3: Image Editing")

    # Create a unique key prefix for this session and step
    key_prefix = f"{st.session_state.current_session}_editing_"
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if 'editing_image' in session:
            display_s3_image(session['editing_image'])
    
    with col2:
        prompt = st.text_input("Text Prompt", key=key_prefix+"prompt", max_chars=2000,
                               help="Describe what you want to add or change in the selected area.")
        negative_prompt = st.text_input("Negative Text Prompt (optional)", key=key_prefix+"negative_prompt", max_chars=2000,
                                        help="Describe what you don't want in the edited area.")
        
        col1, col2 = st.columns(2)
        with col1:
            style_preset = st.selectbox("Style Preset", ["None",
                "photographic", "analog-film", "anime", "cinematic", "comic-book", "digital-art",
                "enhance", "fantasy-art", "isometric", "line-art", "low-poly", "modeling-compound",
                "neon-punk", "origami", "3d-model", "pixel-art", "tile-texture"
            ], key=key_prefix+"style_preset", help="Guides image model towards a particular style. This influences the overall look of the edited area. Default: None")
            style_preset = None if style_preset == "None" else style_preset

        with col2:
            seed = st.number_input("Seed", value=0, min_value=0, max_value=4294967295, key=key_prefix+"seed",
                                   help="Set a seed for reproducible results. Use 0 for random seed. Default: 0")
            if seed == 0:
                seed = random.randint(0, 4294967295)
        drawing_mode = st.selectbox(
            "Drawing Tool", ("freedraw", "line", "rect", "circle", "transform"), key=key_prefix+"drawing_mode",
            help="Choose the drawing tool for creating your mask."
        )

    col1, col2, col3 = st.columns(3)
    with col1:
        brush_size = st.slider("Brush Size", 1, 50, 10, key=key_prefix+"brush_size", help="Adjust the size of the brush.")
    with col2:
        stroke_color = st.color_picker("Stroke Color", "#FFFFFF", key=key_prefix+"stroke_color", help="Choose the color of the brush stroke.")
    with col3:
        fill_color = st.color_picker("Fill Color", "#FFFFFF", key=key_prefix+"fill_color", help="Choose the fill color for shapes.")

    with st.expander("Advanced Settings"):
        col1, col2 = st.columns(2)
        with col1:
            sampler = st.selectbox("Sampler", [
                "DDIM", "DDPM", "K_DPMPP_2M", "K_DPMPP_2S_ANCESTRAL", "K_DPM_2",
                "K_DPM_2_ANCESTRAL", "K_EULER", "K_EULER_ANCESTRAL", "K_HEUN", "K_LMS"
            ], key=key_prefix+"sampler", help="A sampler is a method of generating data in a specific way. Different samplers can produce noticeable different results. The type of sampler chosen affects how the data transformation is performed, from a noisy initial state to a clear and detailed final image. Default: DDIM")
        with col2:
            clip_guidance_preset = st.selectbox("CLIP Guidance Preset", [
                "NONE","FAST_BLUE", "FAST_GREEN", "SIMPLE", "SLOW", "SLOWER", "SLOWEST"
            ], key=key_prefix+"base_clip_guidance_preset", help="A technique that uses the CLIP neural network to guide the generation of images to be more in-line with your included prompt, which often results in improved coherency. Default: NONE")
        cfg_scale = st.slider("CFG Scale", 0, 35, 25, key=key_prefix+"cfg_scale",
                              help="Determines how much the final image portrays the prompt. Lower values = higher randomness. Default: 25")
        steps = st.slider("Steps", 10, 150, 150, key=key_prefix+"steps",
                          help="Determines how many times the image is sampled. More steps can result in a more accurate result with longer processing time. Default: 150")

    # Create a canvas for drawing the mask
    st.write("Draw on the image below:")
    s3 = boto3.client('s3')
    img_data = s3.get_object(Bucket=Config.S3_BUCKET_NAME, Key=session['editing_image'])['Body'].read()
    background_image = Image.open(io.BytesIO(img_data))


    # Calculate the scaling factor and new height
    original_width, original_height = background_image.size
    scale_factor = CANVAS_WIDTH / original_width
    canvas_height = int(original_height * scale_factor)

    # Resize the background image for display
    display_image = background_image.resize((CANVAS_WIDTH, canvas_height), Image.LANCZOS)

    # Create the canvas with the new dimensions
    canvas_result = st_canvas(
        fill_color=fill_color,
        stroke_width=brush_size,
        stroke_color=stroke_color,
        background_image=display_image,
        height=canvas_height,
        width=CANVAS_WIDTH,
        drawing_mode=drawing_mode,
        key=f"canvas_stability_{st.session_state.current_session}",
    )

    if st.button("Apply Editing", disabled=not prompt, help="Missing text prompt" if not prompt else ""):
        if canvas_result.image_data is not None:
            with st.spinner("Applying edits..."):
                # Scale the mask back to the original image size
                mask = canvas_result.image_data[:, :, -1] > 0
                mask = mask.astype(np.uint8) * 255
                mask = cv2.resize(mask, (original_width, original_height), interpolation=cv2.INTER_NEAREST)
                mask_image = Image.fromarray(mask)

                image = stability_model.invoke_image_inpainting(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    init_image=background_image,
                    mask_image=mask_image,
                    style_preset=style_preset,
                    clip_guidance_preset=clip_guidance_preset,
                    seed=seed,
                    cfg_scale=cfg_scale,
                    steps=steps,
                    sampler=sampler
                )
                if image:
                    image_key = save_image_to_s3(image, f"stability_sessions/{st.session_state.current_session}/editing_images")
                    session['editing_images'].append(image_key)
                    save_to_s3(st.session_state.stability_sessions, "stability_sessions")

    st.subheader("Edited Images")
    selected_image_key, selected_index = display_images(session['editing_images'], "editing", allow_remove=True)

    # Update the session with the currently selected image
    if selected_image_key:
        session['selected_editing_image'] = selected_image_key
        session['selected_editing_index'] = selected_index
    else:
        # Remove the selection if no image is selected (e.g., after deletion)
        session.pop('selected_editing_image', None)
        session.pop('selected_editing_index', None)
    
    save_to_s3(st.session_state.stability_sessions, "stability_sessions")

    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back: Image Variation", key="back_to_variation", type="primary"):
            session['step'] = 'variation'
            save_to_s3(st.session_state.stability_sessions, "stability_sessions")
            st.rerun()
    with col2:
        button_disabled = 'selected_editing_image' not in session
        button_type = "secondary" if button_disabled else "primary"
        
        if st.button("Keep Editing", key="keep_editing", type=button_type, disabled=button_disabled):
            if 'selected_editing_image' in session:
                session['editing_image'] = session['selected_editing_image']
                save_to_s3(st.session_state.stability_sessions, "stability_sessions")
                st.rerun()
        
        if 'selected_editing_image' in session:
            st.success("Image Selected")
        else:
            st.error("Please select an image before proceeding.")

# Function to manage model sessions
#
# This function handles the creation, selection, and deletion of user sessions.
# It provides an interface for users to manage their sessions and navigate between them.
# The function also handles saving and loading session data from S3 storage.
#
# Parameters:
# - model: String identifier for the current model (e.g., "stability" or "titan")
# - sessions: Dictionary containing all sessions for the current model
# - model_instance: An instance of the model class (e.g., StabilityModel or TitanModel)
#
# Returns:
# - The current session data if a session is selected, otherwise None
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

        session_names = list(sessions.keys())
        session_names.sort(key=lambda x: sessions[x].get('timestamp', ''), reverse=True)
        session_names.append("New Session")

        def format_func(session_name):
            if session_name == "New Session":
                return f"🆕 New Session"
            else:
                return f"📁 {session_name}"

        selected_session = st.selectbox(
            "Select Session",
            session_names,
            format_func=format_func,
            key=f"{model}_session_select",
            index=session_names.index(st.session_state.current_session) if st.session_state.current_session in session_names else 0
        )

        if selected_session == "New Session":
            new_session_name = st.text_input("Enter new session name")
            if st.button("Create Session") and new_session_name:
                if new_session_name in sessions:
                    st.error(f"Session '{new_session_name}' already exists. Please choose a different name.")
                else:
                    sessions[new_session_name] = {
                        'step': 'base',
                        'base_images': [],
                        'variation_images': [],
                        'editing_images': [],
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

    if getattr(st.session_state, 'show_all_sessions', False):
        display_all_sessions(model, sessions)
        return None

    if st.session_state.current_session not in sessions:
        st.warning("Please select or create a session to continue.")
        return None

    return sessions[st.session_state.current_session]

# Function to display all sessions for a model
#
# This function creates an interface to view all available sessions for a specific model.
# It displays session names, timestamps, and provides options to open or delete sessions.
#
# Parameters:
# - model: String identifier for the current model (e.g., "stability" or "titan")
# - sessions: Dictionary containing all sessions for the current model
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