import json

class ClaudePromptChecker:
    def __init__(self, client, s3_client, bucket_name):
        self.client = client
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.model_id = "anthropic.claude-v2"

    # Send a message to the Claude model and get a response
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
   
    # Analyze a given prompt and provide feedback
    def check_prompt(self, prompt):
        try:
            # Prepare the input for the model, including best practices and instructions
            input_text = f"""As an expert in prompt engineering for image generation models Stability.ai SDXL 1.0 Image Generator and Amazon Titan Image Generator G1, analyze the following prompt:

"{prompt}"

Provide a detailed analysis using the following aspects:

                Prompt Engineering: Best Practices

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


Provide your analysis in the following format:

Strengths:
- [List strengths based on the above criteria]

Areas for Improvement:
- [List areas that need improvement based on the above criteria]

Suggestions:
- [Provide specific, actionable suggestions for enhancing the prompt]

Improved Prompts:
"[Provide an enhanced version of the original prompt, one for Stability and one for Titan, addressing the areas for improvement]"

Negative Prompt Suggestions:
- [Provide 3-5 suggested negative prompts that could be used with this image generation prompt to refine the output]

Explanation:
[Briefly explain the changes made in the improved prompt, referencing the principles of effective prompt engineering. Also, explain the purpose of the suggested negative prompts.]

Be specific, constructive, and provide actionable advice. Ensure your improved prompt example is significantly enhanced and showcases best practices in prompt engineering for both Stability.ai SDXL 1.0 Image Generator and Amazon Titan Image Generator G1."""
            
            # Get the response from the model
            response = self.invoke(input_text)
            if response is None:
                return "I'm sorry, but I'm having trouble analyzing the prompt right now. Please try again later."
            return json.loads(response['body'].read())['completion']
        except Exception as e:
            print(f"Error in check_prompt: {str(e)}")
            return f"An error occurred while analyzing the prompt: {str(e)}"