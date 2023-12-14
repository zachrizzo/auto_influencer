from gradio_client import Client
import random

class ImageGenerator:
    def __init__(self):
        self.client = Client("http://127.0.0.1:7865/")

    def generate_image(self, prompt):
        result = self.client.predict(
            prompt,  # Textbox: prompt
            "",  # Textbox: Negative Prompt
            ["Fooocus V2", "Fooocus Enhance", "Fooocus Sharp"],  # Checkboxgroup: Selected Styles
            "Extreme Speed",  # Radio: Performance
            "1152×896 ∣ 9:7",  # Radio: Aspect Ratios
            1,  # Slider: Image Number (1 to 32)
            random.randint(0, 1000000000),  # Textbox: Seed
            2,  # Slider: Image Sharpness (0.0 to 30.0)
            4,  # Slider: Guidance Scale (1.0 to 30.0)
            "juggernautXL_version6Rundiffusion.safetensors",  # Dropdown: Base Model (SDXL only)
            "None",  # Dropdown: Refiner (SDXL or SD 1.5)
            0.5,  # Slider: Refiner Switch At (0.1 to 1.0)
            "sd_xl_offset_example-lora_1.0.safetensors",  # Dropdown: LoRA 1
            0.1,  # Slider: Weight for LoRA 1 (-2 to 2)
            "None",  # Dropdown: LoRA 2
            1,  # Slider: Weight for LoRA 2 (-2 to 2)
            "None",  # Dropdown: LoRA 3
            1,  # Slider: Weight for LoRA 3 (-2 to 2)
            "None",  # Dropdown: LoRA 4
            1,  # Slider: Weight for LoRA 4 (-2 to 2)
            "None",  # Dropdown: LoRA 5
            1,  # Slider: Weight for LoRA 5 (-2 to 2)
            False,  # Checkbox: Input Image
            "uov",  # Textbox: Parameter 73
            "Disabled",  # Radio: Upscale or Variation
            None,  # Image: Drag Above Image to Here
            [],  # Checkboxgroup: Outpaint Direction
            None,  # Image: Drag Above Image to Here
            "",  # Textbox: Inpaint Additional Prompt
            None,  # Image: Image
            0.5,  # Slider: Stop At (0.0 to 1.0)
            0.6,  # Slider: Weight (0.0 to 2.0)
            "ImagePrompt",  # Radio: Type
            None,  # Image: Image
            0.5,  # Slider: Stop At (0.0 to 1.0)
            0.6,  # Slider: Weight (0.0 to 2.0)
            "ImagePrompt",  # Radio: Type
            None,  # Image: Image
            0.5,  # Slider: Stop At (0.0 to 1.0)
            0.6,  # Slider: Weight (0.0 to 2.0)
            "ImagePrompt",  # Radio: Type
            None,  # Image: Image
            0.5,  # Slider: Stop At (0.0 to 1.0)
            0.6,  # Slider: Weight (0.0 to 2.0)
            "ImagePrompt",  # Radio: Type
            fn_index=30  # Function index for predict
        )
        print(result)

# Example usage
generator = ImageGenerator()
generator.generate_image('a cat on the moon')
