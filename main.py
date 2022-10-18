import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import lab1, lab2

app = FastAPI(title="Information Security")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lab1.lab1Router, prefix="/lab1", tags=["lab1"])
app.include_router(lab2.lab2Router, prefix="/lab2", tags=["lab2"])

if __name__ == '__main__':
    uvicorn.run("main:app", port=5000, log_level="info", reload=True, debug=True)
