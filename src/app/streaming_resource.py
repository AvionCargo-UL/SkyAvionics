import asyncio

import cv2
from fastapi import APIRouter
from starlette.websockets import WebSocket

router = APIRouter()

async def send_video_frames(websocket: WebSocket):
    cap = cv2.VideoCapture(0)  # Change to video file path if using a file
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            await websocket.send_bytes(frame_bytes)
            await asyncio.sleep(0.033)  # About 30 FPS
    finally:
        cap.release()

@router.websocket("/video_streaming")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Receive connection")
    await send_video_frames(websocket)
    await websocket.close()