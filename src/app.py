from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)