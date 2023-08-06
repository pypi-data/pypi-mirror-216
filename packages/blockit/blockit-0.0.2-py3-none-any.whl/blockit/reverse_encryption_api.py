from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class CryptoRequest(BaseModel):
    text: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/encode")
async def encode(request: CryptoRequest):
    request_dict = request.dict()
    reversed_text = request_dict["text"][::-1]
    return {"encoded_text": reversed_text}


@app.post("/decode")
async def decode(request: CryptoRequest):
    request_dict = request.dict()
    reversed_text = request_dict["text"][::-1]
    return {"decoded_text": reversed_text}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
