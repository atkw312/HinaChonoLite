from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from character import generate_chat
from prompt import get_gpt_prompt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

class Params(BaseModel):
    reply: str


class LoadParams(BaseModel):
    name: str

@app.get("/")
def root():
    return {'fastapi api'}

@app.post("/onLoad")
async def onLoad(params: LoadParams):
    global p_template
    p_template = get_gpt_prompt(params.name)
    reply = await generate_chat(prompt=p_template)
    return Response(content=reply, media_type="text/plain")

@app.post("/generate_response")
async def get_text(params: Params):
    global p_template

    prompt = p_template + ' ' + params.reply
    reply = await generate_chat(prompt)
    return Response(content=reply, media_type="text/plain")