import json
import base64
from botocore.exceptions import ClientError
import io
from PIL import Image

class ChatImageEditor:
    def __init__(self, client, s3_client, bucket_name):
        self.client = client
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.model_id = "amazon.titan-image-generator-v1"
    
    # Convert a PIL Image object to a base64 encoded string
    def image_to_base64(self, image):
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Convert a base64 encoded string to a PIL Image object
    def base64_to_image(self, base64_string):
        return Image.open(io.BytesIO(base64.b64decode(base64_string)))

    # Call the Titan model and handle the response
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
            raise
        except Exception as e:
            print(f"ERROR: {e}")
            raise
   
    # Create images from a text description
    def generate_image(self, prompt, num_images=1, width=512, height=512, seed=0, cfg_scale=8.0):
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
        return self.invoke_titan_model(input_params)

    # Edit an existing image with a new text description
    def edit_image(self, prompt, init_image, num_images=1, seed=0, cfg_scale=8.0, mask_prompt=None, outpainting=False):
        task_type = "OUTPAINTING" if outpainting else "INPAINTING"
        params_key = "outPaintingParams" if outpainting else "inPaintingParams"

        input_params = {
            "taskType": task_type,
            params_key: {
                "text": prompt,
                "image": self.image_to_base64(init_image),
                "maskPrompt": mask_prompt or prompt,
            },
            "imageGenerationConfig": {
                "numberOfImages": num_images,
                "cfgScale": cfg_scale,
                "seed": seed,
                "height": init_image.height,
                "width": init_image.width
            }
        }

        if outpainting:
            input_params[params_key]["outPaintingMode"] = "DEFAULT"

        return self.invoke_titan_model(input_params)