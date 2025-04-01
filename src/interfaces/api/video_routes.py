import asyncio
import cv2
from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect
from queue import Queue
import time


def create_video_router(frame_queue: Queue):
    router = APIRouter()

    async def send_video_frames(websocket: WebSocket):
        try:

            # Use a smaller encoding quality for JPEG to reduce size
            encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 65]

            while True:
                if not frame_queue.empty():
                    # Get the most recent frame (discard older frames if multiple are available)
                    frame = None
                    while not frame_queue.empty():
                        frame = frame_queue.get()

                    if frame is not None and frame.size > 0:

                        # Use faster JPEG encoding with lower quality
                        _, buffer = cv2.imencode(".jpg", frame, encode_params)
                        frame_bytes = buffer.tobytes()

                        await websocket.send_bytes(frame_bytes)

                # Shorter sleep interval for higher responsiveness
                await asyncio.sleep(0.040)  # 1ms sleep instead of 40ms
        except WebSocketDisconnect:
            print("Client disconnected")
        except Exception as e:
            print(f"Error in send_video_frames: {e}")

    @router.websocket("/video_streaming")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await send_video_frames(websocket)

    return router
