from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")
OPENAI_PROJECT_ID = os.getenv("OPENAI_PROJECT_ID")
print(OPENAI_API_KEY, OPENAI_ORG_ID, OPENAI_PROJECT_ID) 

client = None

def initialize_fastapi():
    global client
    if not OPENAI_API_KEY:
       raise ValueError("missing openai api key")

    client = OpenAI(
        organization=OPENAI_ORG_ID,
        project=OPENAI_PROJECT_ID,
        api_key=OPENAI_API_KEY
    )


def generate_chat(prompt: str):
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

