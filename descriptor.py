from pathlib import Path
import google.generativeai as genai

genai.configure(api_key="AIzaSyDP20o8c9aoNlns4w49TywukOhXRUNHnxE")

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def generate_description(image_path, instruction):
    # Validate that an image is present
    if not (img := Path(image_path)).exists():
        raise FileNotFoundError(f"Could not find image: {img}")

    image_parts = [
        {
            "mime_type": "image/png",
            "data": Path(image_path).read_bytes()
        },
    ]

    prompt_parts = [

        fr"""
        You are hand-sketch accurate captioning AI, you describe the provided hand Sketches in clear detail to assist the blind in understanding a near accurate look o the dress \n you have been provided with the sketch below :

        # Additional User Instructions:
        {instruction}


        # NOTE:
        Your response should be an text-to-image description of the sketch provided but with photorealistic details to further assist in bringing the same design to life, be very creative and elaborate, description should be a minimum of 200 words and max of 500 words.
        """,
        image_parts[0],
    ]

    response = model.generate_content(prompt_parts)
    return response.text

# image_path = "sketch.png"
# instruction = "Kindly note that this is a dress for better guidance, describe each part of the dress in detail"
# description = generate_description(image_path, instruction)
# print(description)