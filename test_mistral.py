import os
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

key = os.getenv("MISTRAL_API_KEY")

print("Key loaded:", bool(key))

client = Mistral(api_key=key)

response = client.chat.complete(
    model="ministral-3b-2512",
    messages=[
        {"role": "user", "content": "Say hello"}
    ]
)

print(response.choices[0].message.content)