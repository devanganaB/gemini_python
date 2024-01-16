import io
import json
import os
from typing import List
import PIL.Image
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket


load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
# response = chat.send_message([
#     "tell me about moon?"
#     # imgage,
# ], stream=False)

# print(response.text)



app=FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        message = await websocket.recieve()

        if message == "!<FIN>!":
            await websocket.close()
            break
        
        response = chat.send_message([message], stream=True)

    for chunk in response:
        await websocket.send_text(chunk.text)
    await websocket.send_text("<FIN>")


@app.get("/fetch-message", response_model=List[dict])
async def fetch_message():
    return [{"role": message.role, "text": message.parts[0].text} for message in chat.history]

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

