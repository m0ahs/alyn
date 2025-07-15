from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import datetime
import json

app = FastAPI(title="Mem0 Memory API", version="1.0.0")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_store = []  # En mémoire simple

class Memory(BaseModel):
    id: str
    memory: str
    user_id: str
    timestamp: str

class AddMemoryRequest(BaseModel):
    memory: str
    user_id: Optional[str] = "default_user"

@app.post("/mem0/webhook")
async def receive_webhook(request: Request):
    try:
        body = await request.json()
        memory_entry = Memory(
            id=body.get("id", f"mem_{len(memory_store)+1}"),
            memory=body.get("memory", ""),
            user_id=body.get("user_id", "default_user"),
            timestamp=datetime.datetime.utcnow().isoformat()
        )
        memory_store.append(memory_entry)
        return {"status": "ok", "message": "Memory added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing webhook: {str(e)}")

@app.post("/mem0/add")
async def add_memory(request: AddMemoryRequest):
    try:
        memory_entry = Memory(
            id=f"mem_{len(memory_store)+1}",
            memory=request.memory,
            user_id=request.user_id,
            timestamp=datetime.datetime.utcnow().isoformat()
        )
        memory_store.append(memory_entry)
        return {"status": "ok", "message": "Memory added successfully", "memory": memory_entry.dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error adding memory: {str(e)}")

@app.get("/mem0/memories")
def get_memories(user_id: str = "default_user"):
    try:
        filtered_memories = [m.dict() for m in memory_store if m.user_id == user_id]
        return {
            "status": "ok",
            "count": len(filtered_memories),
            "memories": filtered_memories
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving memories: {str(e)}")

@app.get("/")
def root():
    return {
        "message": "Mem0 Memory API",
        "endpoints": {
            "add_memory": "/mem0/add",
            "get_memories": "/mem0/memories",
            "webhook": "/mem0/webhook"
        },
        "docs": "/docs"
    }