from pypdf import PdfReader
from docx import Document
from fastapi import File, UploadFile, HTTPException, status
import io

def extract_pdf_text(data: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(data))
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    except Exception as e:
        raise ValueError(f"Failed to read PDF: {str(e)}")
    
def extract_docx_text(data:bytes) -> str:
    try:
        document = Document(io.BytesIO(data))
        return "\n".join([p.text for p in document.paragraphs])
    except Exception as e:
        raise ValueError(f"Failed to read DOCX: {str(e)}")

def extract_resume_text(file: UploadFile, data: bytes) -> str:
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")
    
    if file.filename and file.filename.lower().endswith(".pdf"):
        return extract_pdf_text(data)
    elif file.filename and file.filename.lower().endswith((".docx", ".doc")):
        return extract_docx_text(data)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF or DOCX.")