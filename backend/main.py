from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI(title="Aegis Guard Backend")


@app.get("/")
async def root():
    return {"status": "ok"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    return JSONResponse({"filename": file.filename, "size": len(contents)})
