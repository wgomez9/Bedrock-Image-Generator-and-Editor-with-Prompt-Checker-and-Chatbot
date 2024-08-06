# Bedrock Image Generator and Editor with Prompt Checker and Chatbot
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

You can iterate through these steps as many times as you like, refining your image until you achieve the desired result.

## 🖼️ Sample Outputs

Below are examples of images generated by each model, demonstrating their capabilities.

### Stability.ai SDXL 1.0 Image Generator Examples

| Fantasy Scene | Superhero | Stylized Nature Scene |
|:---:|:---:|:---:|
| ![Fantasy Scene](images/t1.png) | ![Superhero](images/t2.png) | ![Stylized Nature Scene](images/t3.png) |
| **Prompt:** A majestic dragon perched atop a mountain. There is a rainbow starlit sky and castle in the background. | **Prompt:** batman, cute modern disney style, Pixar 3d portrait, ultra detailed, gorgeous, 3d zbrush, trending on dribbble, 8k render | **Prompt:** A serene Japanese garden in autumn, with a koi pond reflecting a pagoda and falling maple leaves, in the style of Studio Ghibli |

### Amazon Titan Image Generator G1 Examples

| Futuristic Urban Landscape | Detailed Object Rendering | Abstract Concept Visualization |
|:---:|:---:|:---:|
| ![Futuristic Urban Landscape](images/t4.png) | ![Detailed Object Rendering](images/t5.png) | ![Abstract Concept Visualization](images/t6.png) |
| **Prompt:** A futuristic cityscape with flying cars and holographic billboards, bathed in neon lights and light rain | **Prompt:** A steampunk-inspired coffee machine with brass gears and pipes, emitting aromatic steam | **Prompt:** An abstract representation of the concept of time, featuring melting clocks, spiraling galaxies, and streams of binary code |

> Note: The quality and characteristics of generated images can vary based on specific prompts, parameters, and random seed values used.

## 📊 Feature Comparison

| Feature | Description | Stability.ai | Amazon Titan |
|---------|-------------|--------------|--------------|
| Base Image (Text to Image) | Generate images from text descriptions. | ✅ Supported | ✅ Supported |
| Image Variation (Image to Image) | Create variations of an existing image. | ✅ Supported | ✅ Supported |
| Image Editing: Drawing a Mask on Canvas (Image to Image) | Edit parts of an image using a drawn mask. | ✅ Supported | ✅ Supported with Inpainting and Outpainting (Default and Precise) |
| Mask Prompt | Edit image using a prompt to create a mask | ❌ Not available | ✅ Supported |
| Image Upload | Ability to upload images for editing or variation. | ✅ Supported | ✅ Supported |
| Number of Images | Number of images that can be generated in a single request. | ✅ Fixed at 1 | ✅ 1-5 |
| Image Resolution | Pixel width and height. Higher pixel count = higher level of detail. | ✅ 1024x1024, 1152x896, 1216x832, 1344x768, 1536x640, 640x1536, 768x1344, 832x1216, 896x1152 | ✅ 1024x1024, 768x768, 512x512, 1152x896, 1216x832, 1344x768, 1536x640, 1280x768, 1152x640, 1173x640, 896x1152, 832x1216, 768x1344, 640x1536, 768x1280, 640x1152, 640x1173 |
| Text Prompt | Text input to guide image generation. | ✅ Up to 2000 chars | ✅ Up to 512 chars |
| Negative Prompt | Text input to specify unwanted elements in the image. | ✅ Up to 2000 chars | ✅ Up to 512 chars |
| Style Preset | Guides image model towards a particular style. This influences the overall look. | ✅ photographic, analog-film, anime, cinematic, comic-book, digital-art, enhance, fantasy-art, isometric, line-art, low-poly, modeling-compound, neon-punk, origami, 3d-model, pixel-art, tile-texture | ❌ Not available |
| Seed | Number for reproducible image generation. 0 is a random seed. | ✅ 0-4294967295 | ✅ 0-2147483647 |
| CFG Scale | Determines how much the final image portrays the prompt. Lower values = higher randomness. | ✅ 0-35 Scale | ✅ 1.1-10.0 Scale |
| Steps | Determines how many times the image is sampled. More steps can result in a more accurate result with longer processing time. | ✅ 10-150 Scale | ❌ Not available |
| Sampler | Method of generating data in a specific way. Different samplers can produce noticeable different results. | ✅ DDIM, DDPM, K_DPMPP_2M, K_DPMPP_2S_ANCESTRAL, K_DPM_2, K_DPM_2_ANCESTRAL, K_EULER, K_EULER_ANCESTRAL, K_HEUN, K_LMS | ❌ Not available |
| Image Strength/Similarity Strength | Controls how similar the variation is to the original. Higher values = more similar. | ✅ 0-1 Scale | ✅ 0.2-1.0 Scale |
| Clip Guidance Preset | A technique that uses the CLIP neural network to guide the generation of images to be more in-line with your included prompt, which often results in improved coherency. | ✅ FAST_BLUE, FAST_GREEN, NONE, SIMPLE SLOW, SLOWER, SLOWEST | ❌ Not available |
| Extras | Extra parameters passed to the engine. These parameters are used for in-development or experimental features and might change without warning. | ➖ Supported, not included in demo | ❌ Not available |

## 💰 Pricing Information

Current pricing for image generation and text processing through AWS Bedrock:

### Stability AI (SDXL 1.0) Pricing

| Resolution | Quality | Price per Image |
|------------|---------|-----------------|
| Up to 1024x1024 | Standard (<=50 steps) | $0.04 |
| Up to 1024x1024 | Premium (>50 steps) | $0.08 |

### Amazon Titan Pricing

| Resolution | Price per Image |
|------------|-----------------|
| 512x512, 768x768, 1152x640, 1173x640, 640x1152, 640x1173 | $0.0008 |
| 1024x1024, 1152x896, 1216x832, 1344x768, 1536x640, 640x1536, 768x1344, 832x1216, 896x1152, 1280x768, 768x1280 | $0.01 |

### Claude Pricing

Our application is configured with 400 Input Tokens and 800 Output Tokens. The temperature is set to 0.3. While the demo is running Claude 2.0, Claude 3 Sonnet is the recommended model for optimal performance.

| Model | Price per 400 Token Input | Price per 800 Token Output | Total per Input and Output Combined |
|-------|---------------------------|----------------------------|-------------------------------------|
| Claude 3 Sonnet | $0.0012 | $0.012 | $0.0132 |
| Claude 2.0 | $0.0032 | $0.0192 | $0.0224 |

> Note: It's recommended to use Titan to experiment with image generation prompts since it is significantly cheaper than Stability. For text processing and prompt engineering assistance, Claude 3 Sonnet offers better performance at a lower cost compared to Claude 2.0. Prices are subject to change. Always check the [official AWS Bedrock pricing page](https://aws.amazon.com/bedrock/pricing/) for the most up-to-date information.

## ➕ Additional Features

### 🤖 Claude Chatbot Assistant

Our Claude Chatbot Assistant is designed to enhance your image generation experience:
- Engage in interactive conversations to improve your prompts step-by-step by applying prompt engineering techniques
- Generate creative prompt ideas for specific companies or themes
- Get detailed information about Stability.ai SDXL 1.0 and Amazon Titan Image Generator G1
- Learn about pricing, features, and best practices for both models
- Receive guidance on advanced prompt engineering techniques

### ✍️ Prompt Engineering: Best Practices - Prompt Analysis Tool

Our Prompt Analysis is a powerful tool powered by Claude 2.0 to analyze and optimize your image generation prompts:
- Evaluates your prompt's strengths and areas for improvement
- Offers specific suggestions to enhance clarity, detail, and effectiveness
- Provides an improved version of your prompt as an example
- Suggests potential negative prompts to refine your results
- Explains the rationale behind suggested improvements

Use the Prompt Analysis Tool to refine your prompts and achieve better results with both Stability.ai SDXL 1.0 and Amazon Titan Image Generator G1.

> To access the Prompt Analysis Tool and Claude Chatbot Assistant, navigate to the Prompt Engineering: Best Practices and Claude Chatbot Assistant tabs respectively in the application sidebar.

## 📚 Additional Resources

For more information on using these models effectively:

- Consult the AWS Bedrock documentation for detailed API information and best practices
    - [General Bedrock Documentation](https://docs.aws.amazon.com/pdfs/bedrock/latest/userguide/bedrock-ug.pdf)

- Explore the model-specific documentation for Stability.ai SDXL 1.0 Image Generator and Amazon Titan Image Generator G1
    - [Stability.ai SDXL 1.0 Image Generator Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-stability-diffusion.html)
    - [Amazon Titan Image Generator G1 Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-image.html)
    - [Anthropic Claude Models Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-claude.html)

- Experiment with different prompts and settings to understand each model's capabilities and limitations


