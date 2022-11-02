import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import common, lab1, lab2, lab3, lab4

app = FastAPI(title="Information Security")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(common.commonRouter, prefix='/api', tags=['api'])
app.include_router(lab1.lab1Router, prefix='/lab1', tags=['lab1'])
app.include_router(lab2.lab2Router, prefix='/lab2', tags=['lab2'])
app.include_router(lab3.lab3Route, prefix='/lab3', tags=['lab3'])
app.include_router(lab4.lab4Route, prefix='/lab4', tags=['lab4'])

if __name__ == '__main__':
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
