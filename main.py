from fastapi import FastAPI, UploadFile, File, HTTPException
from dotenv import load_dotenv
import httpx
import os

# Инициализация FastAPI приложения
app = FastAPI()

# Загрузка переменных окружения из .env файла
load_dotenv()

# Извлечение Hugging Face токена из окружения
HUGGINGFACE_TOKEN = os.getenv("HF_TOKEN")
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/Falconsai/nsfw_image_detection"

# Основной эндпоинт API: POST /moderate
@app.post("/moderate")
async def moderate_image(file: UploadFile = File(...)):
    # Проверка MIME-типа файла
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Чтение содержимого файла в байты
    image_bytes = await file.read()

    # Базовые заголовки запроса
    headers = {
        "Content-Type": "application/octet-stream",
    }

    if HUGGINGFACE_TOKEN:
        headers["Authorization"] = f"Bearer {HUGGINGFACE_TOKEN}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                HUGGINGFACE_API_URL,
                content=image_bytes,
                headers=headers,
                timeout=60.0 #увеличенный таймаут на случай прогрева модели(чтобы дать подели проснуться)
            )

            # Обработка ошибок ответа
            if response.status_code != 200:
                print("⚠️ Hugging Face response code:", response.status_code)
                print("⚠️ Hugging Face response text:", response.text)
                raise HTTPException(status_code=500, detail="Hugging Face API error")

            # Десериализация JSON-ответа от модели
            results = response.json()
            print("Ответ HF:", results)

            # Извлекаем nsfw_score
            nsfw_score = 0.0
            for item in results:
                if item.get("label") == "nsfw":
                    nsfw_score = item.get("score", 0.0)
                    break

            print("NSFW Score:", nsfw_score)

            if nsfw_score > 0.7:
                return {"status": "REJECTED", "reason": "NSFW content"}
            else:
                return {"status": "OK"}


    except Exception as e:
        # Обработка непредвиденных ошибок
        print("🛑 Внутренняя ошибка:", e)
        raise HTTPException(status_code=500, detail=str(e))
