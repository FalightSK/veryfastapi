from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing_extensions import Annotated

import base64

import torch
from transformers import AutoModel, AutoTokenizer
torch.set_grad_enabled(False)

model_path = '/app/model'
# init model and tokenizer
model = AutoModel.from_pretrained(model_path, trust_remote_code=True).to('cuda').eval()
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get("/testEnd")
async def test_end():
    return "Hello, World!!"

@app.post("/chat")
async def chat(msg: Annotated[str, Form()], file: Annotated[UploadFile, File()] = None):
    # User Input
    query = msg
    
    if file:
        newname = 'img.' + file.filename.split('.')[-1]
        with open(newname, "wb") as buffer:
            buffer.write(await file.read())      
        
        query = "<ImageHere> " + query
        image = 'img.jpg'
        with torch.cuda.amp.autocast():
          response, _ = await model.chat(tokenizer, query=query, image=image,history=[], do_sample=True, temperature=0.3,max_new_tokens=300)
            
        # encoded = None
        # with open(newname, "rb") as img:
        #     encoded = base64.b64encode(img.read())
    else:
        with torch.cuda.amp.autocast():
          response, _ = await model.chat(tokenizer, query=query, history=[], do_sample=True, temperature=0.3,max_new_tokens=300)
    
    return {
        "msg": response,
        "file_content": None
    }