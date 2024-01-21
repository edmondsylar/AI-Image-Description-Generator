#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai
openai.api_type = "azure"
openai.api_base = "https://oaigenesis.openai.azure.com/"
openai.api_version = "2023-06-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Image.create(
    prompt=fr'''try generating an image with this description:  " The dress is a body-hugging, one-shoulder gown with a thigh-high slit. It is made of a luxurious olive green silk fabric and features a daring open back. The dress is simple yet elegant, and it would be perfect for a formal event.  The model in the sketch is wearing a size 6 dress. She is 5'9" tall and weighs 120 pounds. The dress fits her perfectly, and it accentuates her curves beautifully. The dress is also very comfortable, and she can move around in it easily.  The dress is made of a high-quality silk fabric that is soft to the touch and drapes beautifully. The fabric is also very durable, and it will last for years to come. The dress is lined with a soft, cotton fabric that helps to keep the wearer cool and comfortable.  The dress has a one-shoulder neckline that is both stylish and flattering. The shoulder strap is made of the same silk fabric as the dress, and it is wide enough to stay in place comfortably. The dress also has a thigh-high slit that adds a touch of sexiness. The slit is lined with a sheer fabric that helps to prevent it from gaping.  The dress has an open back that is both daring and elegant. The open back is framed by two thin straps that are made of the same silk fabric as the dress. The straps are adjustable, so the wearer can customize the fit of the dress.  The dress is perfect for a formal event, such as a wedding, a gala, or a prom. It is also a great choice for a night out on the town. The dress is sure to turn heads wherever you go."''',
    size='1024x1024',
    n=1
)

image_url = response["data"][0]["url"]