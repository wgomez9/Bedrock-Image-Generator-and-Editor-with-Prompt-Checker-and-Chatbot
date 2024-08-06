import streamlit as st
import pandas as pd

def render_home():
    st.title("🎨 AWS Bedrock Image Generation")
    
    st.write("""
    Welcome to our AWS Bedrock image generation application. This tool allows you to explore and compare 
    two powerful AI image generation models: Stability.ai's SDXL 1.0 Image Generator and Amazon's Titan Image Generator G1.
    Both are available through AWS Bedrock, providing advanced image generation capabilities.
    
    Here's how you can use this application:
    
    1. Select your image generation model on the side bar (SDXL, Titan)
    2. Create or select a session under the image generator model
    3. Generate or upload your base/starting image
    4. Create variations of your image
    5. Edit the image by drawing on it
    6. Switch between your base, variation, and editing steps
    6. For a simplified experience, try Titan Image Chat Editor to use mask prompts
    7. Manage your automatically saved sessions for each of your projects
    
    You can iterate through these steps as many times as you like, refining your image until you achieve the desired result.
    """)
    with st.expander("🎥 Application Walkthrough"):
        st.write("Watch the video below for a detailed walkthrough of the application's features and user experience:")
        st.video("https://www.youtube.com/watch?v=_vdK5PgcNvc")

    with st.expander("🔍 Model Overview"):

        st.subheader("🚀 Stability.ai SDXL 1.0 Image Generator")
        st.write("""
        Stability.ai SDXL 1.0 is an open-source image generation model available through AWS Bedrock. 

        History and Development:
        - Developed by Stability AI, a leader in open-source AI research
        - Released in 2023 as an advancement over previous Stable Diffusion models
        - Integrated into AWS Bedrock to provide enterprise-grade accessibility and scalability

        Qualities:
        - High-quality image generation in virtually any art style
        - Exceptional photorealism capabilities
        - Improved rendering of challenging elements like hands, text, and complex spatial arrangements
        - Enhanced color accuracy, contrast, lighting, and shadows
        - Versatile applications in art creation, creative tooling, and educational contexts
        
        Features:
        - Text-to-Image: Creates images from textual descriptions
        - Image-to-Image: Modifies existing images based on text prompts and reference image
        - Inpainting: Allows editing specific parts of an image
        - Resolution: Supports multiple sizes and aspect rations
        - Style Presets: Offers 17 built-in artistic styles
        - Seed Control: Allows reproducibility with seeds from 0 to 4294967295
        - CFG Scale: Adjustable from 0 to 35 for prompt adherence
        - Steps: Configurable from 10 to 150 for generation refinement
        - Samplers: Multiple options available for different image characteristics
        - Image Strength: Adjustable from 0 to 1 for image variations
        - Clip Guidance Preset: Controls how the model uses CLIP to guide the image generation

        SDXL 1.0 represents a significant leap in image generation technology, offering users control and quality in their creative processes.
        """)

        st.subheader("🦾 Amazon Titan Image Generator G1")
        st.write("""
        Amazon Titan Image Generator G1 is a robust, enterprise-ready image generation model developed by Amazon Web Services (AWS).

        History and Development:
        - Created by Amazon as part of their Titan series of AI models
        - Designed specifically for integration with AWS services and enterprise workflows
        - Developed with a focus on versatility, safety, and scalability

        Qualities:
        - Built-in content filtering for safer outputs
        - Optimized for high-volume, enterprise-level tasks
        - Seamless integration with AWS ecosystem
        
        Features:
        - Text-to-Image: Creates images from textual descriptions 
        - Image-to-Image: Modifies existing images based on text prompts and reference image
        - Inpainting: Allows editing specific parts of an image
        - Outpainting: Replace background or extend bound of an image
        - Prompt as a Mask: Use text to edit images
        - Resolution: Supports multiple sizes
        - Seed Control: Allows reproducibility with seeds from 0 to 2147483647
        - CFG Scale: Adjustable from 1.1 to 10.0 for prompt adherence
        - Multiple Images: Can generate up to 5 variations per request
        - Similarity Strength: Adjustable from 0.2 to 1.0 for image variations
        - Outpainting Modes: Offers 'Default' and 'Precise' options

        Titan Image Generator G1 is engineered to meet the diverse needs of businesses and developers, offering a balance of powerful features and enterprise-grade reliability.
        """)


    with st.expander("🖼️ Sample Outputs"):
        st.write("Below are examples of images generated by each model, demonstrating their capabilities.")

        st.subheader("Stability.ai SDXL 1.0 Image Generator Examples")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("images/t1.png", caption="Fantasy Scene")
            st.markdown("**Prompt:** A majestic dragon perched atop a mountain. There is a rainbow starlit sky and castle in the background.")
        with col2:
            st.image("images/t2.png", caption="Superhero")
            st.markdown("**Prompt:** batman, cute modern disney style, Pixar 3d portrait, ultra detailed, gorgeous, 3d zbrush, trending on dribbble, 8k render")
        with col3:
            st.image("images/t3.png", caption="Stylized Nature Scene")
            st.markdown("**Prompt:** A serene Japanese garden in autumn, with a koi pond reflecting a pagoda and falling maple leaves, in the style of Studio Ghibli")

        st.subheader("Amazon Titan Image Generator G1 Examples")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("images/t4.png", caption="Futuristic Urban Landscape")
            st.markdown("**Prompt:** A futuristic cityscape with flying cars and holographic billboards, bathed in neon lights and light rain")
        with col2:
            st.image("images/t5.png", caption="Detailed Object Rendering")
            st.markdown("**Prompt:** A steampunk-inspired coffee machine with brass gears and pipes, emitting aromatic steam")
        with col3:
            st.image("images/t6.png", caption="Abstract Concept Visualization")
            st.markdown("**Prompt:** An abstract representation of the concept of time, featuring melting clocks, spiraling galaxies, and streams of binary code")

        st.info("Note: The quality and characteristics of generated images can vary based on specific prompts, parameters, and random seed values used.")
   
    with st.expander("📊 Feature Comparison"):
        feature_comparison = {
            'Feature': [
                'Base Image (Text to Image)',
                'Image Variation (Image to Image)',
                'Image Editing: Drawing a Mask on Canvas (Image to Image)',
                'Mask Prompt',
                'Image Upload',
                'Number of Images',
                'Image Resoution', 
                'Text Prompt',
                'Negative Prompt', 
                'Style Preset',
                'Seed',
                'CFG Scale',
                'Steps', 
                'Sampler',
                'Image Strength/Similarity Strenght',
                'Clip Guidance Preset',
                'Extras'                 
            ],
            'Description': [
                'Generate images from text descriptions.',
                'Create variations of an existing image.',
                'Edit parts of an image using a drawn mask.',
                'Edit image using a prompt to create a mask',
                'Ability to upload images for editing or variation.',
                'Number of images that can be generated in a single request.',
                'Pixel width and height. Higher pixel count =  higher level of detail.',
                'Text input to guide image generation.',
                'Text input to specify unwanted elements in the image.',
                'Guides image model towards a particular style. This influences the overall look.',
                'Number for reproducible image generation. 0 is a random seed.',
                'Determines how much the final image portrays the prompt. Lower values = higher randomness.',
                'Determines how many times the image is sampled. More steps can result in a more accurate result with longer processing time.',
                'Method of generating data in a specific way. Different samplers can produce noticeable different results.',
                'Controls how similar the variation is to the original. Higher values = more similar.',      
                'A technique that uses the CLIP neural network to guide the generation of images to be more in-line with your included prompt, which often results in improved coherency.',
                'Extra parameters passed to the engine. These parameters are used for in-development or experimental features and might change without warning.'
            ],
            'Stability.ai': [
                '✅ Supported',
                '✅ Supported',
                '✅ Supported',
                '❌ Not available',
                '✅ Supported',
                '✅ Fixed at 1',
                '✅ 1024x1024, 1152x896, 1216x832, 1344x768, 1536x640, 640x1536, 768x1344, 832x1216, 896x1152',
                '✅ Up to 2000 chars',
                '✅ Up to 2000 chars',
                '✅ photographic, analog-film, anime, cinematic, comic-book, digital-art, enhance, fantasy-art, isometric, line-art, low-poly, modeling-compound, neon-punk, origami, 3d-model, pixel-art, tile-texture',
                '✅ 0-4294967295',
                '✅ 0-35 Scale',
                '✅ 10-150 Scale',
                '✅ DDIM, DDPM, K_DPMPP_2M, K_DPMPP_2S_ANCESTRAL, K_DPM_2, K_DPM_2_ANCESTRAL, K_EULER, K_EULER_ANCESTRAL, K_HEUN, K_LMS',
                '✅ 0-1 Scale',
                '✅ FAST_BLUE, FAST_GREEN, NONE, SIMPLE SLOW, SLOWER, SLOWEST',
                '➖ Supported, not included in demo'
            ],
            'Amazon Titan': [
                '✅ Supported',
                '✅ Supported',
                '✅ Supported with Inpainting and Outpainting (Default and Precise)',
                '✅ Supported',               
                '✅ Supported',
                '✅ 1-5',
                '✅ 1024x1024, 768x768, 512x512, 1152x896, 1216x832, 1344x768, 1536x640, 1280x768, 1152x640, 1173x640, 896x1152, 832x1216, 768x1344, 640x1536, 768x1280, 640x1152, 640x1173',
                '✅ Up to 512 chars',
                '✅ Up to 512 chars',
                '❌ Not available',
                '✅ 0-2147483647',
                '✅ 1.1-10.0 Scale',
                '❌ Not available',
                '❌ Not available',
                '✅ 0.2-1.0 Scale',
                '❌ Not available',
                '❌ Not available'

            ]
        }
        
        df_features = pd.DataFrame(feature_comparison)
        st.table(df_features.set_index('Feature'))
    
    with st.expander("💰 Pricing Information"):
        st.write("Current pricing for image generation through AWS Bedrock:")

        st.subheader("Stability AI (SDXL 1.0) Pricing")
        stability_pricing = pd.DataFrame({
            'Resolution': ['Up to 1024x1024', 'Up to 1024x1024'],
            'Quality': ['Standard (<=50 steps)', 'Premium (>50 steps)'],
            'Price per Image': ['$0.04', '$0.08']
        })
        st.table(stability_pricing)

        st.subheader("Amazon Titan Pricing")
        titan_pricing = pd.DataFrame({
            'Resolution': ['512x512, 768x768, 1152x640, 1173x640, 640x1152, 640x1173',
                        '1024x1024, 1152x896, 1216x832, 1344x768, 1536x640, 640x1536, 768x1344, 832x1216, 896x1152, 1280x768, 768x1280'],
            'Price per Image': ['$0.0008', '$0.01']
        })
        st.table(titan_pricing)

        st.write("Note: Recommended to use Titan to experiment with prompts since it is significanlty cheaper than Stability. Prices are subject to change. Always check the official AWS Bedrock pricing page (https://aws.amazon.com/bedrock/pricing/)for the most up-to-date information.")

    with st.expander("➕ Additional Features"):

        st.subheader("🤖 Claude Chatbot Assistant")
        st.write("""
        Our Claude Chatbot Assistant is designed to enhance your image generation experience:
        - Engage in interactive conversations to improve your prompts step-by-step by applying prompt engineering techniques
        - Generate creative prompt ideas for specific companies or themes
        - Get detailed information about Stability.ai SDXL 1.0 and Amazon Titan Image Generator G1
        - Learn about pricing, features, and best practices for both models
        - Receive guidance on advanced prompt engineering techniques

        """)

        st.subheader("✍️ Prompt Engineering: Best Practices - Prompt Analysis Tool")
        st.write("""
        Our Prompt Analysis is a powerful tool powered by Claude 2.0 to analyze and optimize your image generation prompts:
        - Evaluates your prompt's strengths and areas for improvement
        - Offers specific suggestions to enhance clarity, detail, and effectiveness
        - Provides an improved version of your prompt as an example
        - Suggests potential negative prompts to refine your results
        - Explains the rationale behind suggested improvements

        Use the Prompt Analysis Tool to refine your prompts and achieve better results with both Stability.ai SDXL 1.0 and Amazon Titan Image Generator G1.
        """)

        st.info("To access the Prompt Analysis Tool and Claude Chatbot Assistant, navigate to the Prompt Engineering: Best Practices and Claude Chatbot Assistant tabs respectively in the application sidebar.")

    with st.expander("📚 Additional Resources"):
        st.write("""
        For more information on using these models effectively:

        - Consult the AWS Bedrock documentation for detailed API information and best practices
            - General Bedrock Documentation: https://docs.aws.amazon.com/pdfs/bedrock/latest/userguide/bedrock-ug.pdf
        
        - Explore the model-specific documentation for Stability.ai SDXL 1.0 Image Generator and Amazon Titan Image Generator G1
            - Stability.ai SDXL 1.0 Image Generator Documentation: https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-stability-diffusion.html
                 
            - Amazon Titan Image Generator G1 Documentation: https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-image.html
            
            - Anthropic Claude Models Documentation: https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-claude.html
                 
        - Experiment with different prompts and settings to understand each model's capabilities and limitations
        """)

if __name__ == "__main__":
    render_home()
 

