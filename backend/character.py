from openai import OpenAI

# try:
#     from mykey import OPENAI_KEY
#     print("🔑 Using OPENAI_KEY from mykey.py")
# except ImportError:
#     from keys import OPENAI_KEY
#     print("🔑 Using OPENAI_KEY from keys.py (fallback)")

chat_history = []
OPENAI_KEY = ""

client = None


def set_key(k):
    global OPENAI_KEY, client  # Access global variables
    if k and isinstance(k, str) and k.strip():  # Ensure the key is valid (non-empty string)
        OPENAI_KEY = k  # Update key
        client = OpenAI(
            organization='org-8mp3GqL065se45HMQDqJwI5q',
            project='proj_1a4a7U3ioBOQSsmXTu7WWIIR',
            api_key=OPENAI_KEY
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
        # print(chunk.choices[0].delta.content, end="")
  chat_history.append(full_response)

  return full_response

