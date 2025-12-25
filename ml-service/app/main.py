from fastapi import FastAPI

app = FastAPI(title= "Autoslide ml service")

@app.get("/")
def health_check():
    return {"status": "ml service is running"}