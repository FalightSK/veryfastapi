import uvicorn
from fastapi import FastAPI, File, UploadFile
from typing_extensions import Annotated

app = FastAPI()

@app.get("/test-end/")
async def test_end():
    return "Hello, World!!"


if __name__ == "__main__":
    uvicorn.rum(app, host="0.0.0.0", port=8000)