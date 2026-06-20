from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import edge_tts
import io

app = FastAPI()

@app.get("/api/tts")
async def text_to_speech(text: str = Query(..., description="စာသား ထည့်ရန်"), voice: str = Query("my-MM-NilarNeural", description="အသံရွေးရန်")):
    try:
        communicate = edge_tts.Communicate(text, voice)
        audio_stream = io.BytesIO()
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_stream.write(chunk["data"])
                
        audio_stream.seek(0)
        return StreamingResponse(audio_stream, media_type="audio/mpeg")
    except Exception as e:
        return {"error": str(e)}
