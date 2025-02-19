import asyncio
import cv2
from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect
from queue import Queue
import time
from src.configuration.service_locator import ServiceLocator

def create_video_router(frame_queue: Queue):
    router = APIRouter()

    async def send_video_frames(websocket: WebSocket):
        try:
            # Keep track of latency
            frame_send_count = 0
            last_report_time = time.time()
            
            # Use a smaller encoding quality for JPEG to reduce size
            encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
            
            while True:
                if not frame_queue.empty():
                    # Get the most recent frame (discard older frames if multiple are available)
                    frame = None
                    while not frame_queue.empty():
                        frame = frame_queue.get()
                    
                    if frame is not None and frame.size > 0:
                        # Resize frame if it's too large (optional)
                        # height, width = frame.shape[:2]
                        # if width > 640:
                        #     frame = cv2.resize(frame, (640, int(height * 640 / width)))
                        
                        # Use faster JPEG encoding with lower quality
                        _, buffer = cv2.imencode('.jpg', frame, encode_params)
                        frame_bytes = buffer.tobytes()
                        
                        await websocket.send_bytes(frame_bytes)
                        
                        # Calculate metrics
                        frame_send_count += 1
                        current_time = time.time()
                        if current_time - last_report_time > 5.0:
                            fps = frame_send_count / (current_time - last_report_time)
                            print(f"Sending at {fps:.1f} FPS")
                            frame_send_count = 0
                            last_report_time = current_time
                
                # Shorter sleep interval for higher responsiveness
                await asyncio.sleep(0.001)  # 1ms sleep instead of 40ms
        except WebSocketDisconnect:
            print("Client disconnected")
        except Exception as e:
            print(f"Error in send_video_frames: {e}")

    @router.websocket("/video_streaming")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        print("WebSocket client connected")
        await send_video_frames(websocket)

    return router