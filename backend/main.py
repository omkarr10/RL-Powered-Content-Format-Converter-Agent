
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.convert import router as convert_router

app = FastAPI(title="RL-Powered Content Format Converter")
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)
app.include_router(convert_router)
