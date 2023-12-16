import os
import random
import base64
from PIL import Image
from io import BytesIO
from gradio_client import Client
import asyncio
import time

class ImageGenerator:
    def __init__(self):
        self.client = Client("http://127.0.0.1:7865/", serialize=False)


    def _convert_img_to_base64(self, img_path):
        with Image.open(img_path) as image:
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode()

    async def continuous_img_gen(self, prompt, negative_prompt, performance, number_of_photos, img_prompt, img_face_path, img_face_stop_at, img_face_weight, img_prompt_1_path, img_prompt_stop_at_1, img_prompt_weight_1):
        img_face_base64 = self._convert_img_to_base64(img_face_path)

        img_1_files = [os.path.join(img_prompt_1_path, file) for file in os.listdir(img_prompt_1_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
        for img_path in img_1_files:
            img_prompt_base64 = self._convert_img_to_base64(img_path)

            result =  await self.client.predict(
                prompt, negative_prompt, ['Fooocus V2', 'Fooocus Enhance', 'Fooocus Sharp'], performance, '1152×896 <span style="color: grey;"> ∣ 9:7</span>', number_of_photos, random.randint(0, 2**63 - 1), 2, 4, 'juggernautXL_version6Rundiffusion.safetensors', 'None', 0.5, 'sd_xl_offset_example-lora_1.0.safetensors', 0.1, 'None', 1, 'None', 1, 'None', 1, 'None', 1, img_prompt, 'uov', 'Disabled', None, [], None, '', img_face_base64, img_face_stop_at, img_face_weight, 'FaceSwap', img_prompt_base64, img_prompt_stop_at_1, img_prompt_weight_1, 'ImagePrompt', None, 0.5, 0.6, 'ImagePrompt', None, 0.5, 0.6, 'ImagePrompt',
                fn_index=30
            )

            while result is None:
                time.sleep(1)

            print("Predict result type:", type(result))
            print("Predict result content:", result)




    def generate_image(self, prompt, image_path):
        # Convert the image to a Base64 encoded string
        image_base64 = self._convert_img_to_base64(image_path)

        # Prediction logic with the Base64 encoded image
        result = self.client.predict(
            prompt, '', ['Fooocus V2', 'Fooocus Enhance', 'Fooocus Sharp'], 'Extreme Speed', '1152×896 <span style="color: grey;"> ∣ 9:7</span>', 1, '3876750373260134344', 2, 4, 'juggernautXL_version6Rundiffusion.safetensors', 'None', 0.5, 'sd_xl_offset_example-lora_1.0.safetensors', 0.1, 'None', 1, 'None', 1, 'None', 1, 'None', 1, False, 'uov', 'Disabled', None, [], None, '', image_base64, 0.5, 0.6, 'ImagePrompt', None, 0.5, 0.6, 'ImagePrompt', None, 0.5, 0.6, 'ImagePrompt', None, 0.5, 0.6, 'ImagePrompt',
            fn_index=30  # Function index for predict
        )

        return result



# Example usage
# generator = ImageGenerator()
# generator.generate_image('a cat on the moon')
