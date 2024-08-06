import json

class ClaudeChatbot:
    def __init__(self, client, s3_client, bucket_name):
        self.client = client
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.model_id = "anthropic.claude-v2"

    def invoke(self, input_text):
        prompt = f"\n\nHuman: {input_text}\n\nAssistant:"
        body = {
            "prompt": prompt,
            "max_tokens_to_sample": 800,
            "temperature": 0.3,
        }
        body = json.dumps(body)
        try:
            response = self.client.invoke_model(
                body=body,
                modelId=self.model_id,
                accept='application/json',
                contentType='application/json'
            )
            return response
        except Exception as e:
            print(f"ERROR: {e}")
            return None

    def get_chatbot_response(self, message, conversation_history, conversation_mode):
        try:
            formatted_history = ""
            for msg in conversation_history:
                if msg["role"] == "user":
                    formatted_history += f"Human: {msg['content']}\n\n"
                else:
                    formatted_history += f"Assistant: {msg['content']}\n\n"
            
            prompt_engineering_principles = """
                Prompt Engineering: Best Practices Content

                Mastering prompt engineering is crucial for leveraging AI image generation models effectively. This guide explores key principles and advanced techniques to craft prompts that yield precise, high-quality outputs from models like Stability.ai SDXL 1.0 Image Generator and Amazon Titan Image Generator G1.
                
                1. Specificity is Key
                Provide detailed descriptions including subject, style, colors, lighting, and composition. The more precise your prompt, the closer the output will match your vision.
                Include:
                * Subject description: Main focus of the image
                * Style and medium: E.g., "oil painting", "digital art", "photograph"
                * Color palette: Specific color descriptions
                * Lighting: Type and quality of light in the scene
                * Composition: Viewpoint, framing, and layout
                * Mood and atmosphere: Emotional tone of the image
                Example: "A serene mountain landscape at sunset, with snow-capped peaks reflecting orange and pink hues from the sky. Foreground features a winding river with crystal-clear water. Oil painting style with thick, textured brushstrokes."
               
                2. Leverage Descriptive Language
                Use vivid, concrete words to paint a clear picture. Avoid vague terms in favor of specific, evocative language.
                * Use sensory details: Describe textures, sounds, and even implied scents
                * Employ metaphors and similes for complex concepts
                * Choose precise adjectives and verbs
                Example: Instead of "beautiful flower", use "a vibrant red rose with velvety petals, glistening with morning dew, its stem adorned with emerald leaves reaching towards the golden sunlight."
                
                3. Establish Tone and Atmosphere
                Set the mood through carefully chosen words that reflect the desired emotional context or style of the image.
                * Use emotive language to convey feelings
                * Describe the overall ambiance
                * Consider cultural or historical context
                Example: "A melancholic scene of an abandoned amusement park on a foggy autumn morning. Rusted Ferris wheel looms in the background, while fallen leaves carpet the cracked pathways. The atmosphere is heavy with nostalgia and the passage of time."
                
                4. Structure for Clarity
                Organize your prompt logically for better interpretation by the AI:
                * Use punctuation to separate distinct elements
                * Order descriptions from general to specific
                * Group related concepts together
                Example: "Portrait of a young woman: red hair, green eyes | Wearing: vintage 1950s floral dress | Setting: sunlit garden with blooming roses | Style: impressionist painting | Mood: serene and contemplative"
                
                5. Utilize Negative Prompts
                Specify what you don't want to see in the image. This helps refine the output by explicitly excluding unwanted elements.
                * Be specific about undesired features or qualities
                * Use to avoid common AI artifacts
                * Can help maintain artistic integrity
                Example: Negative prompt: "blurry, distorted, extra limbs, unnatural proportions, text, watermarks, oversaturated colors, anime style"
                
                6. Iterate and Refine
                Treat prompt creation as an iterative process. Analyze results and adjust your prompts based on the outputs you receive.
                    1. Start with a basic prompt
                    2. Analyze the generated image
                    3. Identify areas for improvement or refinement
                    4. Adjust the prompt accordingly
                    5. Regenerate and reassess
                    6. Repeat until desired outcome is achieved
                Tip: Keep a log of prompts and corresponding outputs to track improvements and learn from each iteration.
                
                7. Optimal Prompt Length
                For Stability AI SDXL, aim for prompts between 75-100 words. For Amazon Titan, keep prompts under 512 characters.
                * Start with the most important elements and add details progressively
                * Use sentence fragments for efficiency, focusing on descriptive phrases
                * Balance between being comprehensive and avoiding redundancy
                * Effective prompts tend to be detailed but not overly long

                8. Specify Medium and Style
                Clearly state the desired artistic medium and any specific style references.
                * Mention traditional media: oil painting, watercolor, charcoal sketch
                * Specify digital techniques: 3D rendering, pixel art, vector illustration
                * Reference art movements or artists for style guidance
                Example: "A cityscape in the style of Van Gogh's 'Starry Night', rendered as a digital illustration with bold, swirling brush strokes and vibrant, contrasting colors."
                
                9. Include Composition Details
                Mention viewpoints and compositional elements to guide image structure.
                * Specify camera angles: bird's-eye view, worm's-eye view, Dutch angle
                * Mention composition techniques: rule of thirds, golden ratio, leading lines
                * Describe depth and perspective: foreground, middle ground, background elements
                Example: "A wide-angle shot of a bustling marketplace, with a fish-eye lens effect. Foreground shows detailed vendor stalls, middle ground captures the crowd, and background reveals distant architecture. Use leading lines of market aisles to draw the eye through the scene."
                
                10. Describe Lighting
                Specify lighting conditions for more control over the atmosphere and mood.
                * Mention natural light sources: soft morning light, harsh midday sun, golden hour
                * Describe artificial lighting: candlelight, neon signs, studio lighting setups
                * Use lighting to enhance mood: dramatic shadows, diffused glow, backlit silhouettes
                Example: "A portrait lit by candlelight, with strong chiaroscuro effects. Soft, warm light illuminates one side of the subject's face, casting deep, mysterious shadows on the other side. Background is shrouded in darkness, focusing attention on the subject."
                
                Advanced Techniques:
                1. Weighted Prompts
                Use parentheses and colons to assign weights to different elements of your prompt:
                * The format is (element : weight) where weight is typically between 0.5 and 1.5
                * Higher weights increase emphasis, lower weights decrease it
                Example: "(red roses:1.2) in a (crystal vase:0.8) on a (mahogany table:1.0)"
                
                2. Style Mixing
                Combine multiple artistic styles or influences:
                * Use percentage or ratio indicators for style blending
                * Reference specific artists or art movements
                Example: "A portrait in the style of (Van Gogh:60%) and (Picasso:40%)"
                
                3. Technical Parameters
                Incorporate technical details for more control:
                * Camera settings: lens type, focal length, aperture
                * Lighting setup: soft boxes, rim lighting, color gels
                * Post-processing effects: HDR, color grading, film grain
                Example: "Portrait of a man, 85mm lens, f/1.8 aperture, soft box lighting, slight Kodachrome color grading"
                
                Best Practices for Amazon Titan Image Generator:
                1. Image Generation
                * Start prompts with "An image of..." for better context setting
                * Provide detailed descriptions, including medium, color, lighting, style, and quality
                * Use specific prompts and consider negative prompts when applicable
                * Avoid negative words in negative text prompts (e.g, Instead of "no mirrors", just type "mirrors")
                * Use double quotes for text within images (e.g., "An image of a sign that says "Hello"")

                2. Image Variation
                * Intended to generate a new image that preserves the content of the input image but varies it a little.
                * Describe the original image accurately in the prompt
                * Specify details you want to preserve from the original image
                * At minimum, describe the main object(s) of interest in the scene
                * More detailed and richer prompts help preserve more elements from the original image
                * Avoid describing elements not present in the original image
                * Adjust Similarity Strength if the image is too different or alike to the original image

                3. Inpainting and Outpainting
                * For inpainting object removal, use an empty text prompt
                * For inpainting object replacement, be precise about what to reconstruct, including unique features 
                    * Optionally include context/background details for more realistic reconstruction
                * For outpainting, provide a detailed description of the desired background 
                    * Sometimes describe the whole scene, including objects inside the mask, for better results
                * Adjust brush size, stroke color, and fill color for precise masking

                4. Mask Prompt
                * Be precise and detailed about the object(s) to segment
                * Specify unique attributes/features to focus the segmentation algorithm
                * For complex scenes, use specific descriptors to isolate the desired object

                5. General Tips
                * Effective prompts tend to be detailed but not overly long, providing key visual features, styles, emotions or other descriptive elements
                * Adjust cfg_scale to control prompt adherence and ensure good constrainment of the model
                * Use a seed of zero to randomize the seed and get different results almost every time a new image is generated without changing the settings

                Best Practices and Resources for Stability.ai SDXL 1.0 Image Generator:
                1. Image Generation
                * Start prompts with the subject, then add detailed imagery, environment, mood, and style
                * Experiment with resolutions; wider aspect ratios often yield more realistic human faces
                * Add negative prompts without negative words
                * Avoid conflicting styles such as putting "pixel art" in the text prompt and "photographic" as the style preset

                2. Image Variation
                * Adjust Image Strength if the image is too different or alike to the original image
                * Provide a text prompt to guide the direction of the variation

                3. Image Editing
                * Be precise about what to reconstruct inside the mask region
                * Include context/background details for more realistic reconstruction
                * Adjust brush size, stroke color, and fill color for precise masking
                * Higher cfg scale and step values often yield better results for inpainting
                * For more consistent results, keep the same style preset across the steps or select none
                * If an edit failed, focus on increasing steps, redrawing the mask, wording the prompt differently, and adjusting cfg scale (iterate and refine)

                4. General Tips
                * Effective prompts tend to be detailed but not overly long, providing key visual features, styles, emotions or other descriptive elements
                * Adjust cfg_scale to control prompt adherence and ensure good constrainment of the model
                * Use a seed of zero to randomize the seed and get different results almost every time a new image is generated without changing the settings
                * Experiment with different samplers and clip guidance preset options for varied results
                * Use higher step values (e.g., 50-150) for more refined outputs, balancing quality and generation time
                * Experiment with style presets: 'Photographic' and 'Cinematic' styles often work well for realistic human faces

            """
    
            model_info = """

                    🎨 AWS Bedrock Image Generation
                    Welcome to our AWS Bedrock image generation application. This tool allows you to explore and compare two powerful AI image generation models: Stability.ai's SDXL 1.0 Image Generator and Amazon's Titan Image Generator G1. Both are available through AWS Bedrock, providing advanced image generation capabilities.
                    Here's how you can use this application:

                    1. Select your image generation model on the side bar (SDXL, Titan)
                    2. Create or select a session under the image generator model
                    3. Generate or upload your base/starting image
                    4. Create variations of your image
                    5. Edit the image by drawing on it
                    6. Switch between your base, variation, and editing steps
                    7. For a simplified experience, try Titan Image Chat Editor to use mask prompts
                    8. Manage your automatically saved sessions for each of your projects

                    🔍 Model Overview
                    🚀 Stability.ai SDXL 1.0 Image Generator
                    Stability.ai SDXL 1.0 is an open-source image generation model available through AWS Bedrock.
                    History and Development:

                    * Developed by Stability AI, a leader in open-source AI research
                    * Released in 2023 as an advancement over previous Stable Diffusion models
                    * Integrated into AWS Bedrock to provide enterprise-grade accessibility and scalability

                    Qualities:

                    * High-quality image generation in virtually any art style
                    * Exceptional photorealism capabilities
                    * Improved rendering of challenging elements like hands, text, and complex spatial arrangements
                    * Enhanced color accuracy, contrast, lighting, and shadows
                    * Versatile applications in art creation, creative tooling, and educational contexts

                    Features:

                    * Text-to-Image: Creates images from textual descriptions
                    * Image-to-Image: Modifies existing images based on text prompts and reference image
                    * Inpainting: Allows editing specific parts of an image
                    * Resolution: Supports multiple sizes and aspect rations
                    * Style Presets: Offers 17 built-in artistic styles
                    * Seed Control: Allows reproducibility with seeds from 0 to 4294967295
                    * CFG Scale: Adjustable from 0 to 35 for prompt adherence
                    * Steps: Configurable from 10 to 150 for generation refinement
                    * Samplers: Multiple options available for different image characteristics
                    * Image Strength: Adjustable from 0 to 1 for image variations
                    * Clip Guidance Preset: Controls how the model uses CLIP to guide the image generation

                    SDXL 1.0 represents a significant leap in image generation technology, offering users control and quality in their creative processes.

                    🦾 Amazon Titan Image Generator G1
                    Amazon Titan Image Generator G1 is a robust, enterprise-ready image generation model developed by Amazon Web Services (AWS).
                    History and Development:

                    * Created by Amazon as part of their Titan series of AI models
                    * Designed specifically for integration with AWS services and enterprise workflows
                    * Developed with a focus on versatility, safety, and scalability

                    Qualities:

                    * Built-in content filtering for safer outputs
                    * Optimized for high-volume, enterprise-level tasks
                    * Seamless integration with AWS ecosystem

                    Features:

                    * Text-to-Image: Creates images from textual descriptions
                    * Image-to-Image: Modifies existing images based on text prompts and reference image
                    * Inpainting: Allows editing specific parts of an image
                    * Outpainting: Replace background or extend bound of an image
                    * Prompt as a Mask: Use text to edit images
                    * Resolution: Supports multiple sizes
                    * Seed Control: Allows reproducibility with seeds from 0 to 2147483647
                    * CFG Scale: Adjustable from 1.1 to 10.0 for prompt adherence
                    * Multiple Images: Can generate up to 5 variations per request
                    * Similarity Strength: Adjustable from 0.2 to 1.0 for image variations
                    * Outpainting Modes: Offers 'Default' and 'Precise' options

                    Titan Image Generator G1 is engineered to meet the diverse needs of businesses and developers, offering a balance of powerful features and enterprise-grade reliability.

                    Feature Comparison

                    1. Base Image (Text to Image) Description: Generate images from text descriptions. Stability.ai: Supported / Amazon Titan: Supported
                    2. Image Variation (Image to Image) Description: Create variations of an existing image. Stability.ai: Supported / Amazon Titan: Supported
                    3. Image Editing: Drawing a Mask on Canvas (Image to Image) Description: Edit parts of an image using a drawn mask. Stability.ai: Supported / Amazon Titan: Supported with Inpainting and Outpainting (Default and Precise)
                    4. Mask Prompt Description: Edit image using a prompt to create a mask Stability.ai: Not available / Amazon Titan: Supported
                    5. Image Upload Description: Ability to upload images for editing or variation. Stability.ai: Supported / Amazon Titan: Supported
                    6. Number of Images Description: Number of images that can be generated in a single request. Stability.ai: Fixed at 1 / Amazon Titan: 1-5
                    7. Image Resolution Description: Pixel width and height. Higher pixel count = higher level of detail. Stability.ai: 1024x1024, 1152x896, 1216x832, 1344x768, 1536x640, 640x1536, 768x1344, 832x1216, 896x1152 / Amazon Titan: 1024x1024, 768x768, 512x512, 1152x896, 1216x832, 1344x768, 1536x640, 1280x768, 1152x640, 1173x640, 896x1152, 832x1216, 768x1344, 640x1536, 768x1280, 640x1152, 640x1173
                    8. Text Prompt Description: Text input to guide image generation. Stability.ai: Up to 2000 chars / Amazon Titan: Up to 512 chars
                    9. Negative Prompt Description: Text input to specify unwanted elements in the image. Stability.ai: Up to 2000 chars / Amazon Titan: Up to 512 chars
                    10. Style Preset Description: Guides image model towards a particular style. This influences the overall look. Stability.ai: photographic, analog-film, anime, cinematic, comic-book, digital-art, enhance, fantasy-art, isometric, line-art, low-poly, modeling-compound, neon-punk, origami, 3d-model, pixel-art, tile-texture / Amazon Titan: Not available
                    11. Seed Description: Number for reproducible image generation. 0 is a random seed. Stability.ai: 0-4294967295 / Amazon Titan: 0-2147483647
                    12. CFG Scale Description: Determines how much the final image portrays the prompt. Lower values = higher randomness. Stability.ai: 0-35 Scale / Amazon Titan: 1.1-10.0 Scale
                    13. Steps Description: Determines how many times the image is sampled. More steps can result in a more accurate result with longer processing time. Stability.ai: 10-150 Scale / Amazon Titan: Not available
                    14. Sampler Description: Method of generating data in a specific way. Different samplers can produce noticeable different results. Stability.ai: DDIM, DDPM, K_DPMPP_2M, K_DPMPP_2S_ANCESTRAL, K_DPM_2, K_DPM_2_ANCESTRAL, K_EULER, K_EULER_ANCESTRAL, K_HEUN, K_LMS / Amazon Titan: Not available
                    15. Image Strength/Similarity Strength Description: Controls how similar the variation is to the original. Higher values = more similar. Stability.ai: 0-1 Scale / Amazon Titan: 0.2-1.0 Scale
                    16. Clip Guidance Preset Description: A technique that uses the CLIP neural network to guide the generation of images to be more in-line with your included prompt, which often results in improved coherency. Stability.ai: FAST_BLUE, FAST_GREEN, NONE, SIMPLE SLOW, SLOWER, SLOWEST /  Amazon Titan: Not available
                    17. Extras Description: Extra parameters passed to the engine. These parameters are used for in-development or experimental features and might change without warning. Stability.ai: Supported, not included in demo / Amazon Titan: Not available

                    Pricing Information

                    Stability AI (SDXL 1.0) Pricing:
                    Resolution: Up to 1024x1024 Quality: Standard (<=50 steps) Price per Image: $0.04
                    Resolution: Up to 1024x1024 Quality: Premium (>50 steps) Price per Image: $0.08

                    Amazon Titan Pricing:
                    Resolution: 512x512, 768x768, 1152x640, 1173x640, 640x1152, 640x1173 Price per Image: $0.0008
                    Resolution: 1024x1024, 1152x896, 1216x832, 1344x768, 1536x640, 640x1536, 768x1344, 832x1216, 896x1152, 1280x768, 768x1280 Price per Image: $0.01

                    Note: Prices are subject to change. Always check the official AWS Bedrock pricing page for the most up-to-date information.

                    ➕ Additional Features
                    🤖 Claude Chatbot Assistant Our Claude Chatbot Assistant is designed to enhance your image generation experience:

                    * Engage in interactive conversations to improve your prompts step-by-step by applying prompt engineering techniques
                    * Generate creative prompt ideas for specific companies or themes
                    * Get detailed information about Stability.ai SDXL 1.0 and Amazon Titan Image Generator G1
                    * Learn about pricing, features, and best practices for both models
                    * Receive guidance on advanced prompt engineering techniques

                    ✍️ Prompt Engineering: Best Practices - Prompt Analysis Tool Our Prompt Analysis is a powerful tool powered by Claude 2.0 to analyze and optimize your image generation prompts:

                    * Evaluates your prompt's strengths and areas for improvement
                    * Offers specific suggestions to enhance clarity, detail, and effectiveness
                    * Provides an improved version of your prompt as an example
                    * Suggests potential negative prompts to refine your results
                    * Explains the rationale behind suggested improvements

                    Use the Prompt Analysis Tool to refine your prompts and achieve better results with both Stability.ai SDXL 1.0 and Amazon Titan Image Generator G1.
                    To access the Prompt Analysis Tool and Claude Chatbot Assistant, navigate to the Prompt Engineering: Best Practices and Claude Chatbot Assistant tabs respectively in the application sidebar.
                    
                    📚 Additional Resources
                    For more information on using these models effectively:

                    * Consult the AWS Bedrock documentation for detailed API information and best practices 
                        * General Bedrock Documentation: https://docs.aws.amazon.com/pdfs/bedrock/latest/userguide/bedrock-ug.pdf
                    * Explore the model-specific documentation for Stability.ai SDXL 1.0 Image Generator and Amazon Titan Image Generator G1 
                        * Stability.ai SDXL 1.0 Image Generator Documentation: https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-stability-diffusion.html
                        * Amazon Titan Image Generator G1 Documentation: https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-image.html
                        * Anthropic Claude Models Documentation: https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-claude.html
                    * Experiment with different prompts and settings to understand each model's capabilities and limitations



            """
    
            if conversation_mode == "improve_prompt":
                system_message = f"""You are an AI assistant specialized in helping users improve their prompts for image generation. 
                Use the following principles and best practices to guide your suggestions:
    
                {prompt_engineering_principles}
    
                Model-Specific Information:
                {model_info}
    
                Analyze the user's prompt and ask the user one question at a time to refine the prompt, 
                focusing on adding specificity, descriptive language, and relevant details. Big emphasize on giving the user one question at a time. Do not overwhelm the user with several questions at once. Suggest improvements based on the model-specific 
                best practices depending on whether the user is using Stability.ai SDXL 1.0 or Amazon Titan Image Generator G1. Once you have gathered enough information to generate a good prompt, give a final suggested prompt 
                and ask the user if they wish to continue to have a one question at a time chat improving the prompt further with more additonal descriptive elements. Do not get off-topic"""
    
            elif conversation_mode == "generate_idea":
                system_message = f"""You are an AI assistant specialized in generating creative prompt ideas for image generation. 
                Use the following principles and best practices to guide your suggestions:
    
                {prompt_engineering_principles}
    
                Model-Specific Information:
                {model_info}
    
                Act as a marketing expert to create compelling, detailed prompts based on the user's company or theme. 
                Incorporate relevant brand elements, style preferences, and target audience considerations into your prompt ideas. 
                Tailor your suggestions to either Stability.ai SDXL 1.0 or Amazon Titan Image Generator G1 based on the user's preference. Do not get off-topic."""
    
            elif conversation_mode == "answer_questions":
                system_message = f"""You are an AI assistant specialized in answering questions about Stability.ai SDXL 1.0 and Amazon Titan Image Generator G1. 
                Provide accurate information about their features, pricing, and best practices. Use the following information as a reference, do not give mis-information from other sources. Stick with this source:
    
                {prompt_engineering_principles}
    
                Model-Specific Information:
                {model_info}
    
                When discussing prompt engineering techniques, refer to the principles and best practices listed above. Do not get off-topic and be concise with your responses"""
    
            input_text = f"{system_message}\n\n{formatted_history}Human: {message}\n\nAssistant:"
            
            response = self.invoke(input_text)
            if response is None:
                return "I'm sorry, but I'm having trouble generating a response right now. Please try again later."
            return json.loads(response['body'].read())['completion']
        except Exception as e:
            print(f"Error in get_chatbot_response: {str(e)}")
            return f"An error occurred: {str(e)}"