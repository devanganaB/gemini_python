import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
response = chat.send_message([
    "tell me about moon?"
    # imgage,
], stream=False)

for chunk in response:
    print(chunk.text, end="")