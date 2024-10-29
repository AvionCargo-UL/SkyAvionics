import uvicorn
from fastapi import FastAPI

from src.app.streaming_resource import router as streaming_router

from starlette.middleware.cors import CORSMiddleware


def launch():
    print("Launching app...")
    app = __setup_app()
    uvicorn.run(app, host="127.0.0.1", port=8080)

def __setup_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(streaming_router)

    return app
