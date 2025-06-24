import rasterio
import numpy as np
from PIL import Image
import base64
import openai
import json
import io

openai.api_key = "YOUR_OPENAI_API_KEY"
tif_path = "your_tile.tif"  # Replace with the path to your raster file


with rasterio.open(tif_path) as src:
    band = src.read(1)  # Use the first band
    profile = src.profile

    # Normalize to 0–255 for PNG
    norm_band = ((band - band.min()) / (band.max() - band.min()) * 255).astype(np.uint8)


img = Image.fromarray(norm_band)
buffered = io.BytesIO()
img.save(buffered, format="PNG")
img_bytes = buffered.getvalue()
b64_image = base64.b64encode(img_bytes).decode()

response = openai.ChatCompletion.create(
    model="gpt-4-vision-preview",  # Or "gpt-4o"
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": (
                    "This is a satellite or elevation image of a potential archaeological site. "
                    "Please identify any features like geometric shapes, circular mounds, straight lines, or terracing "
                    "that may indicate past human activity. For each identified feature, provide a confidence score (0–100). "
                    "Respond in the following JSON format:\n"
                    "{\n  \"features\": [\n    {\"name\": \"...\", \"description\": \"...\", \"confidence\": 0}\n  ]\n}"
                )
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{b64_image}"
                }
            }
        ]
    }],
    max_tokens=800
)

reply = response['choices'][0]['message']['content']

# Try to parse as JSON if possible
try:
    parsed = json.loads(reply)
    for feature in parsed["features"]:
        print(f" {feature['name']} ({feature['confidence']}%): {feature['description']}")
except Exception as e:
    print("Raw GPT Response (not valid JSON):")
    print(reply)