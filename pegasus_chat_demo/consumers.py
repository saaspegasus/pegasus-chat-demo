import json
import uuid

from channels.generic.websocket import WebsocketConsumer
from django.conf import settings
from django.template.loader import render_to_string
from openai import OpenAI


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.messages = []
        super().connect()

    def receive(self, text_data):
        # our webhook handling code goes here
        text_data_json = json.loads(text_data)
        message_text = text_data_json["message"]
        # do something with the user's message
        # show user's message
        user_message_html = render_to_string(
            "pegasus_chat_demo/ws/chat_message.html",
            {
                "message_text": message_text,
                "is_system": False,
            },
        )
        self.send(text_data=user_message_html)
        self.messages.append(
            {
                "role": "user",
                "content": message_text,
            }
        )
        message_id = f"message-{uuid.uuid4().hex}"
        system_message_html = render_to_string(
            "pegasus_chat_demo/ws/chat_message.html",
            {"message_text": "", "is_system": True, "message_id": message_id},
        )
        self.send(text_data=system_message_html)

        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        openai_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            stream=True,
        )
        chunks = []
        for chunk in openai_response:
            message_chunk = (chunk.choices[0].delta.content or "").replace("\n", "<br>")
            self.send(text_data=f'<div id="{message_id}" hx-swap-oob="beforeend">{message_chunk}</div>')
            chunks.append(message_chunk)
        self.messages.append({"role": "system", "content": "".join(chunks)})
