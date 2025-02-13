from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")
OPENAI_PROJECT_ID = os.getenv("OPENAI_PROJECT_ID")
print(OPENAI_API_KEY, OPENAI_ORG_ID, OPENAI_PROJECT_ID)  # Test

client = None


def set_key(k):
    global OPENAI_KEY, client
    if k and isinstance(k, str) and k.strip():
        OPENAI_KEY = k 
        client = OpenAI(
            organization=OPENAI_ORG_ID,
            project=OPENAI_PROJECT_ID,
            api_key=OPENAI_API_KEY
        )
        print("✅ OpenAI key updated successfully.")
    else:
        print("⚠️ Invalid OpenAI key. Key was not updated.")
  

async def generate_chat(prompt: str):
  stream = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "user", "content": prompt}],
      stream=True,
  )

  full_response = ""
  for chunk in stream:
      if chunk.choices[0].delta.content is not None:
        full_response += chunk.choices[0].delta.content

  return full_response

