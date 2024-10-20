import json
import uuid

from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from src.svg_gem.router.image_router import router as image_router
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from utility.langchain_helper.simple_factory_type import SocketEvent
from utility.websocket.websocket_manager import websocket_manager

load_dotenv()

app = FastAPI(openapi_url="/docs/openapi.json", docs_url="/docs")

app.include_router(image_router)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"version": "0.0.1"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    g_socket_id = str(uuid.uuid4())
    await websocket_manager.connect(g_socket_id, websocket)
    try:
        await websocket.send_text(json.dumps({'event': SocketEvent.open, '_id': g_socket_id}))
        while True:
            data = await websocket.receive_json()
    except WebSocketDisconnect:
        print('websocket disconnect user '+g_socket_id)
        websocket_manager.disconnect(g_socket_id)
