import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(title="Devel Lab AI Service")

LLM_URL = os.getenv("LLM_ENDPOINT", "https://llm-internal.softex:9001")

class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    response: str
    status: str

@app.get("/")
def health_check():
    return {"status": "ok", "service": "running", "host": "0.0.0.0:8080"}

@app.post("/generate", response_model=PromptResponse)
async def generate_text(payload: PromptRequest):
    # Tratamento defensivo de chamadas HTTP para o endpoint sandbox
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(
                f"{LLM_URL}/v1/completions",
                json={"prompt": payload.prompt}
            )
            res.raise_for_status()
            data = res.json()
            # Adaptação textual para infraestruturas sem tool-calling nativo
            return PromptResponse(response=data.get("text", ""), status="success")
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503, 
            detail="Serviço LLM indisponível no ambiente de rede atual."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))