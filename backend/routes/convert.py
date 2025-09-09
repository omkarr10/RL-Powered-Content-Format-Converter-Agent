from fastapi import APIRouter, UploadFile, Form, Response
from fastapi.responses import FileResponse, JSONResponse
from agent.converter import convert_content
import os

router = APIRouter()

@router.post("/convert-content")
async def convert_content_api(
    input_file: UploadFile = None,
    input_text: str = Form(None),
    input_type: str = Form(...),
    output_type: str = Form(...),
):
    result = await convert_content(input_file, input_text, input_type, output_type)
    
    if "error" in result:
        return JSONResponse(content=result)
        
    # If the result contains a file path, serve it as a downloadable file
    if isinstance(result["converted_content"], str) and os.path.exists(result["converted_content"]):
        file_path = result["converted_content"]
        filename = os.path.basename(file_path)
        
        # Set appropriate content type
        content_type = "audio/mpeg" if output_type == "audio" else "video/mp4" if output_type == "video" else "text/plain"
        
        # Return file for download
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type=content_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    # Return JSON for text content or metadata
    return JSONResponse(content=result)
