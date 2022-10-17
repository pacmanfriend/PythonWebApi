import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import lab1

app = FastAPI(title="Information Security")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lab1.testRouter, prefix="/lab1", tags=["lab1"])

if __name__ == '__main__':
    uvicorn.run("main:app", port=5000, log_level="info", reload=True, debug=True)
