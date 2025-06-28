# NSFW Image Moderation API (на FastAPI)

Простое backend-приложение на FastAPI, которое принимает изображение и проверяет его на наличие NSFW-контента через Hugging Face модель `Falconsai/nsfw_image_detection`.

## Что делает

- Принимает изображение (`.jpg`, `.png`) через POST-запрос
- Отправляет его в модель NSFW-детекции
- Возвращает:
  - `{"status": "OK"}` — если изображение безопасное
  - `{"status": "REJECTED", "reason": "NSFW content"}` — если обнаружен NSFW-контент

## Установка зависимостей:

```bash
pip install -r requirements.txt
```

## Структура проекта
```bash
.
├── main.py
├── .env
├── requirements.txt
├── README.md
└── images/
    └── example.jpg
```

Создай файл .env и вставь свой Hugging Face токен:
```bash
HF_TOKEN=hf_ваш_токен_здесь
```
Токен можно получить бесплатно здесь: https://huggingface.co/settings/tokens

## Запуск сервера:
```bash
uvicorn main:app --reload
```

## Пример запроса (изображение example.jpg)
```bash
curl -X POST -F "file=@images/example.jpg" http://localhost:8000/moderate
```
или если запускать через PowerShell
```bash
curl.exe -X POST -F "file=@images/example.png" http://localhost:8000/moderate
```

## Пример ответа

Если изображение безопасное:
```bash
{"status": "OK"}
```
Если найден NSFW-контент:
```bash
{"status": "REJECTED", "reason": "NSFW content"}
```