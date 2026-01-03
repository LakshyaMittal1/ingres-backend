from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

print("API KEY =", os.getenv("GROQ_API_KEY"))

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Explain groundwater contamination in simple terms."}
    ],
)

print(response.choices[0].message.content)
