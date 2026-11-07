from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "FastAPI Demo is running successfully"}


@app.get("/health")
def health():
    return {"status": "healthy"}
