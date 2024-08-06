import json
import base64
from botocore.exceptions import ClientError
import io
from PIL import Image

class TitanModel:
    def __init__(self, client, s3_client, bucket_name):
        self.client = client
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.model_id = "amazon.titan-image-generator-v1"

    def image_to_base64(self, image):
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def base64_to_image(self, base64_string):
        return Image.open(io.BytesIO(base64.b64decode(base64_string)))

    def invoke_titan_model(self, input_params):
        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(input_params).encode('utf-8')
            )
            response_body = json.loads(response.get("body").read())
            return [self.base64_to_image(img) for img in response_body.get("images", [])]
        except ClientError as e:
            print(f"ERROR: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
            return None
        except Exception as e:
            print(f"ERROR: {e}")
            return None

    def invoke_titan_text_to_image(self, prompt, negative_prompt, num_images, width, height, seed, cfg_scale):
        input_params = {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": prompt,
            },
            "imageGenerationConfig": {
                "numberOfImages": num_images,
                "height": height,
                "width": width,
                "cfgScale": cfg_scale,
                "seed": seed
            }
        }
        if negative_prompt:
            input_params["textToImageParams"]["negativeText"] = negative_prompt
        return self.invoke_titan_model(input_params)

    def invoke_titan_image_variation(self, prompt, negative_prompt, init_image, similarity_strength, num_images, seed, cfg_scale):
        input_params = {
            "taskType": "IMAGE_VARIATION",
            "imageVariationParams": {
                "text": prompt,
                "images": [self.image_to_base64(init_image)],
                "similarityStrength": similarity_strength,
            },
            "imageGenerationConfig": {
                "numberOfImages": num_images,
                "cfgScale": cfg_scale,
                "seed": seed
            }
        }
        if negative_prompt:
            input_params["imageVariationParams"]["negativeText"] = negative_prompt
        return self.invoke_titan_model(input_params)

    def invoke_titan_inpainting(self, prompt, negative_prompt, init_image, mask_image, num_images, seed, cfg_scale):
        input_params = {
            "taskType": "INPAINTING",
            "inPaintingParams": {
                "image": self.image_to_base64(init_image),
                "text": prompt,
                "maskImage": self.image_to_base64(mask_image),
            },
            "imageGenerationConfig": {
                "numberOfImages": num_images,
                "cfgScale": cfg_scale,
                "seed": seed
            }
        }
        if negative_prompt:
            input_params["inPaintingParams"]["negativeText"] = negative_prompt
        return self.invoke_titan_model(input_params)
    
    def invoke_titan_outpainting(self, prompt, negative_prompt, init_image, mask_image, num_images, seed, cfg_scale, outpainting_mode):
        input_params = {
            "taskType": "OUTPAINTING",
            "outPaintingParams": {
                "text": prompt,
                "image": self.image_to_base64(init_image),
                "maskImage": self.image_to_base64(mask_image),
                "outPaintingMode": outpainting_mode
            },
            "imageGenerationConfig": {
                "numberOfImages": num_images,
                "cfgScale": cfg_scale,
                "seed": seed
            }
        }
        if negative_prompt:
            input_params["outPaintingParams"]["negativeText"] = negative_prompt
        return self.invoke_titan_model(input_params)