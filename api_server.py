from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_workflow import process_content_request
from revision_workflow import process_revision_request

app = FastAPI(title="PR Content API", version="1.0.0")

class ContentRequest(BaseModel):
    input_text: str
    input_type: str = "email"

class RevisionRequest(BaseModel):
    feedback_text: str

@app.post("/generate-content")
async def generate_content(request: ContentRequest):
    try:
        result = process_content_request(
            input_text=request.input_text,
            input_type=request.input_type
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/revise-content")  
async def revise_content(request: RevisionRequest):
    try:
        result = process_revision_request(request.feedback_text)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "PR API running"}

@app.get("/")
async def root():
    return {"message": "PR Content Automation API", "version": "1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
 