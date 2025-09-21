
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.convert import router as convert_router
from routes.feedback import router as feedback_router
import time

app = FastAPI(title="RL-Powered Content Format Converter")
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
	expose_headers=["*"],
)
app.include_router(convert_router)
app.include_router(feedback_router)


@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestration."""
    return {"status": "healthy", "service": "rl-converter"}

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    try:
        response = await call_next(request)
        return response
    finally:
        duration_ms = int((time.time() - start) * 1000)
        path = request.url.path
        method = request.method
        print(f"{method} {path} - {duration_ms}ms")
