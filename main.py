from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import httpx
#import os

app = FastAPI()

# 💡 Сюда вставь свой ключ
DEEPAI_API_KEY = "dce4fd4d-8fce-4cd7-9166-cf85f215f268"
DEEPAI_URL = "https://api.deepai.org/api/nsfw-detector"

@app.post("/moderate")
async def moderate_image(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    try:
        # Создаём асинхронного клиента
        async with httpx.AsyncClient() as client:
            response = await client.post(
                DEEPAI_URL,
                files={"image": (file.filename, await file.read())},
                headers={"api-key": DEEPAI_API_KEY}
            )

        # Проверяем, что всё прошло успешно
        if response.status_code != 200:
            print("Код ответа DeepAI:", response.status_code)
            print("Тело ответа DeepAI:", response.text)
            raise HTTPException(status_code=500, detail="DeepAI error")

        data = response.json()

        # Извлекаем nsfw_score
        nsfw_score = data.get("output", {}).get("nsfw_score", 0)

        if nsfw_score > 0.7:
            return {"status": "REJECTED", "reason": "NSFW content"}

        return {"status": "OK"}

    except Exception as e:
        print("Ошибка при обращении к DeepAI:", e)
        raise HTTPException(status_code=500, detail=str(e))

