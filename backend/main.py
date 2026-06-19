from dotenv import load_dotenv
load_dotenv()

import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from backend.apis.text_analyze import router as text_router
from backend.apis.voice_analyze import router as voice_router
from backend.apis.video_analyze import router as video_router
from backend.apis.multimodal import router as multimodal_router
from backend.apis.stress import router as stress_router
from backend.apis.mood import router as mood_router     # ✅ MUST
from backend.apis.events import router as events_router
from backend.apis.recommendation import router as recommendation_router
from backend.utils.db import init_db
from backend.apis.trends import router as trends_router
from backend.apis.dashboard import router as dashboard_router
from backend.apis.alerts import router as alert_router
from backend.apis.chat import router as chat_router
from backend.apis.wearable import router as wearable_router
from backend.apis.privacy import router as privacy_router
from backend.apis.reminder import router as reminder_router
from backend.apis.calendar import router as calendar_router
from backend.apis.voice_chat import router as voice_chat_router
from backend.apis.chat_gpt import router as gpt_chat_router
from backend.apis.reward import router as reward_router
from backend.apis.streak import router as streak_router
from backend.utils.db import get_recent_events, get_reward_status, get_streak

app = FastAPI(title="Emotional Care AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

# ✅ ROUTERS (ORDER DOESN'T MATTER BUT MUST EXIST)
app.include_router(text_router)
app.include_router(voice_router)
app.include_router(video_router)
app.include_router(multimodal_router)
app.include_router(stress_router)
app.include_router(mood_router)        # 🔥 THIS LINE FIXES IT
app.include_router(events_router)
app.include_router(recommendation_router)
app.include_router(trends_router)
app.include_router(dashboard_router)
app.include_router(alert_router)
app.include_router(chat_router)
app.include_router(wearable_router)
app.include_router(privacy_router)
app.include_router(reminder_router)
app.include_router(calendar_router)
app.include_router(voice_chat_router)
app.include_router(gpt_chat_router)
app.include_router(reward_router)
app.include_router(streak_router)

@app.get("/")
def root():
    return {"message": "Emotional Care backend running"}


@app.websocket("/ws/realtime-emotion")
async def realtime_emotion_socket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            events = get_recent_events(limit=25)
            await websocket.send_json(
                {
                    "type": "dashboard_update",
                    "timestamp": events[0]["timestamp"] if events else None,
                    "events": events,
                    "reward": get_reward_status(),
                    "streak": get_streak(),
                }
            )
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        return
