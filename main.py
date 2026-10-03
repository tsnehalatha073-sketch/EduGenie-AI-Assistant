import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from jinja2 import Environment, FileSystemLoader, select_autoescape

from config import is_demo, status, get_active_model
from qna import answer_question
from explanation_module import explain_topic
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

# Direct Jinja2 environment - no Starlette TemplateResponse, no version issues
jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)


@asynccontextmanager
async def lifespan(app):
    print("")
    print("=" * 58)
    print("   EduGenie - Google Gemini Powered Learning Assistant")
    print("=" * 58)
    if is_demo():
        print("   MODE  : DEMO (no valid API key)")
        print("   FIX   : add GOOGLE_API_KEY in .env, then restart")
    else:
        print("   MODE  : LIVE")
        print("   MODEL : " + str(get_active_model()))
    print("   URL   : http://127.0.0.1:8000")
    print("   DOCS  : http://127.0.0.1:8000/docs")
    print("=" * 58)
    print("")
    yield


app = FastAPI(
    title="EduGenie - AI Learning Assistant",
    description="Gemini powered Q&A, Explanation, Summary, Quiz and Learning Paths",
    version="2.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class QuestionIn(BaseModel):
    question: str = ""


class TopicIn(BaseModel):
    topic: str = ""


class TextIn(BaseModel):
    text: str = ""


FALLBACK_HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>EduGenie</title></head>
<body style="font-family:Arial;padding:40px">
<h2>EduGenie</h2>
<p style="color:#b00">templates/index.html was not found.</p>
<p>Create the file <b>templates/index.html</b> and refresh.</p>
<p>API still works: <a href="/docs">/docs</a> | <a href="/health">/health</a></p>
</body></html>"""


@app.get("/", response_class=HTMLResponse)
async def home():
    try:
        template = jinja_env.get_template("index.html")
        html = template.render(
            demo_mode=is_demo(),
            model=get_active_model() or "demo",
        )
        return HTMLResponse(content=html, status_code=200)
    except Exception as exc:
        print("[EduGenie] Template error:", exc)
        return HTMLResponse(content=FALLBACK_HTML, status_code=200)


@app.get("/health")
async def health():
    data = {"status": "ok"}
    data.update(status())
    return data


@app.get("/models")
async def models():
    return status()


# ---------------- Q and A ----------------
@app.get("/qa")
async def qa_get(question: str = Query(...)):
    return {"question": question, "answer": answer_question(question)}


@app.post("/qa")
async def qa_post(body: QuestionIn):
    if not body.question.strip():
        return JSONResponse({"error": "Please provide a question."}, status_code=400)
    return {"question": body.question, "answer": answer_question(body.question)}


# ---------------- Explain ----------------
@app.get("/explain")
async def explain_get(topic: str = Query(...)):
    return {"topic": topic, "explanation": explain_topic(topic)}


@app.post("/explain")
async def explain_post(body: TopicIn):
    if not body.topic.strip():
        return JSONResponse({"error": "Please provide a topic."}, status_code=400)
    return {"topic": body.topic, "explanation": explain_topic(body.topic)}


# ---------------- Summarize ----------------
@app.post("/summarize")
async def summarize_post(body: TextIn):
    if not body.text.strip():
        return JSONResponse({"error": "Please provide text to summarize."}, status_code=400)
    return {"summary": summarize_text(body.text)}


# ---------------- Quiz ----------------
@app.get("/quiz")
async def quiz_get(text: str = Query(...)):
    return {"quiz": generate_quiz(text)}


@app.post("/quiz")
async def quiz_post(body: TextIn):
    if not body.text.strip():
        return JSONResponse({"error": "Please provide a topic for the quiz."}, status_code=400)
    return {"quiz": generate_quiz(body.text)}


# ---------------- Learning Path ----------------
@app.get("/learn/recommendations")
async def learn_get(topic: str = Query(...)):
    return {"topic": topic, "recommendation": get_learning_recommendations(topic)}


@app.post("/learn/recommendations")
async def learn_post(body: TopicIn):
    if not body.topic.strip():
        return JSONResponse({"error": "Please provide a topic."}, status_code=400)
    return {"topic": body.topic, "recommendation": get_learning_recommendations(body.topic)}