from fastapi import FastAPI, UploadFile, File, HTTPException
from backend.app.services.resume_parser import extract_text_from_pdf
import os
import uuid

app = FastAPI(
    title="AI Job & Career Intelligence Agent",
    version="1.0.0"
)

UPLOAD_DIR = "data/resumes"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Job & Career Intelligence Agent"
    }


@app.post("/resumes/upload")
async def upload_resume(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    file_id = str(uuid.uuid4())

    file_path = os.path.join(
        UPLOAD_DIR,
        f"{file_id}.pdf"
    )

    file_content = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(file_content)

    extracted_text = extract_text_from_pdf(file_path)

    return {
        "filename": file.filename,
        "file_id": file_id,
        "text": extracted_text
    }
