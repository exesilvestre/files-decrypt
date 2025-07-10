from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from middleware import LimitUploadSizeMiddleware
from utils.constants import MAX_UPLOAD_SIZE
from endpoints.upload_router import router as upload_router
from endpoints.file_query_router import router as file_router

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(LimitUploadSizeMiddleware, max_upload_size=MAX_UPLOAD_SIZE)
app.include_router(upload_router)
app.include_router(file_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
