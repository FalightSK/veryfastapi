from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing_extensions import Annotated

import base64

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
    if file:
        newname = 'img.' + file.filename.split('.')[-1]
        print(newname)
        with open(newname, "wb") as buffer:
            buffer.write(await file.read())
            
        encoded = None
        with open(newname, "rb") as img:
            encoded = base64.b64encode(img.read())
    return {
        "msg": "สวัสดีครับ" + msg,
        "file_content": encoded if file is not None else None
    }