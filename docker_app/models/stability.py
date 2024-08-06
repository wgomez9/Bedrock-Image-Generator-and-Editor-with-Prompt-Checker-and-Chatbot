import json
import base64
from botocore.exceptions import ClientError
import io
from PIL import Image

class StabilityModel:
    def __init__(self, client, s3_client, bucket_name):
        self.client = client
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.model_id = "stability.stable-diffusion-xl-v1"

    # Convert an image to a base64 string
    def image_to_base64(self, image):
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    # Convert a base64 string to an image
    def base64_to_image(self, base64_string):
        return Image.open(io.BytesIO(base64.b64decode(base64_string)))

    # Call the Stability model and handle the response
    def invoke_stability_model(self, input_params):
        try:
            if input_params.get('style_preset') is None:
                input_params.pop('style_preset', None)
            response = self.client.invoke_model(
                modelId=self.model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(input_params).encode('utf-8')
            )
            response_body = json.loads(response.get("body").read())
            image_data = response_body.get("artifacts", [])[0]
            return self.base64_to_image(image_data["base64"])
        except ClientError as e:
            print(f"ERROR: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
            return None
        except Exception as e:
            print(f"ERROR: {e}")
            return None

    # Generate an image from a text prompt
    def invoke_text_to_image(self, prompt, negative_prompt, width, height, style_preset, clip_guidance_preset, seed, cfg_scale, steps, sampler):
        input_params = {
            "text_prompts": [
                {"text": prompt, "weight": 1},
                {"text": negative_prompt, "weight": -1}
            ],
            "cfg_scale": cfg_scale,
            "height": height,
            "width": width,
            "samples": 1,
            "steps": steps,
            "style_preset": style_preset,
            "clip_guidance_preset": clip_guidance_preset,
            "seed": seed,
            "sampler": sampler
        }
        return self.invoke_stability_model(input_params)

    # Create a variation of an existing image
    def invoke_image_variation(self, prompt, negative_prompt, init_image, image_strength, style_preset, clip_guidance_preset, seed, cfg_scale, steps, sampler):
        input_params = {
            "text_prompts": [
                {"text": prompt, "weight": 1},
                {"text": negative_prompt, "weight": -1}
            ],
            "init_image": self.image_to_base64(init_image),
            "init_image_mode": "IMAGE_STRENGTH",
            "image_strength": image_strength,
            "cfg_scale": cfg_scale,
            "samples": 1,
            "steps": steps,
            "style_preset": style_preset,
            "clip_guidance_preset": clip_guidance_preset,
            "seed": seed,
            "sampler": sampler
        }
        return self.invoke_stability_model(input_params)

    # Perform inpainting on an image
    def invoke_image_inpainting(self, prompt, negative_prompt, init_image, mask_image, style_preset, clip_guidance_preset, seed, cfg_scale, steps, sampler):
        input_params = {
            "text_prompts": [
                {"text": prompt, "weight": 1},
                {"text": negative_prompt, "weight": -1}
            ],
            "init_image": self.image_to_base64(init_image),
            "mask_source": "MASK_IMAGE_WHITE",
            "mask_image": self.image_to_base64(mask_image),
            "cfg_scale": cfg_scale,
            "samples": 1,
            "seed": seed,
            "steps": steps,
            "style_preset": style_preset,
            "clip_guidance_preset": clip_guidance_preset,
            "sampler": sampler
        }
        return self.invoke_stability_model(input_params)