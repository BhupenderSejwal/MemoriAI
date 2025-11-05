from fastapi import FastAPI

app = FastAPI(title="MemoriAI Cognitive MVP")

@app.get("/")
def read_root():
    return {"message": "Cognitive Service running"}

@app.post("/cognitive/ask")
def ask(q: str):
    return {"answer": f"Answer to '{q}' (placeholder)"}
