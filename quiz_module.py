import re
import json
from config import generate_text, is_demo


def clean_json_block(text):
    """Remove markdown fences and isolate the JSON array."""
    text = (text or "").strip()
    text = re.sub(r"```(?:json)?\s*(.*?)\s*```", r"\1", text, flags=re.DOTALL).strip()
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]
    return text.strip()


def _validate(data):
    valid = []
    if not isinstance(data, list):
        return valid
    for item in data:
        if not isinstance(item, dict):
            continue
        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        answer = str(item.get("answer", "")).strip()
        if not question or not isinstance(options, list) or len(options) != 4:
            continue
        options = [str(o).strip() for o in options]
        if answer not in options:
            match = None
            for o in options:
                if o.lower() == answer.lower():
                    match = o
                    break
            if match is None:
                continue
            answer = match
        valid.append({"question": question, "options": options, "answer": answer})
    return valid


def _demo_quiz(text):
    topic = (text or "General Knowledge").strip()[:70]
    t = topic.lower()

    if "pythagor" in t or "theorem" in t:
        return [
            {
                "question": "What does the Pythagorean theorem describe?",
                "options": [
                    "The relationship between the angles of a triangle",
                    "The relationship between the sides of a right angled triangle",
                    "The relationship between area and perimeter of a triangle",
                    "The relationship between the sides of any triangle",
                ],
                "answer": "The relationship between the sides of a right angled triangle",
            },
            {
                "question": "If a and b are the shorter sides and c is the hypotenuse, which equation is correct?",
                "options": ["a + b = c", "a^2 + b^2 = c^2", "a^2 - b^2 = c^2", "2a + 2b = 2c"],
                "answer": "a^2 + b^2 = c^2",
            },
            {
                "question": "Which type of triangle does the Pythagorean theorem apply to?",
                "options": [
                    "Equilateral triangles",
                    "Isosceles triangles",
                    "Right angled triangles",
                    "All types of triangles",
                ],
                "answer": "Right angled triangles",
            },
        ]

    if "solar" in t or "planet" in t or "space" in t:
        return [
            {
                "question": "How many planets are in our Solar System?",
                "options": ["6", "7", "8", "9"],
                "answer": "8",
            },
            {
                "question": "Which planet is closest to the Sun?",
                "options": ["Venus", "Mars", "Mercury", "Earth"],
                "answer": "Mercury",
            },
            {
                "question": "Which is the largest planet in our Solar System?",
                "options": ["Saturn", "Jupiter", "Neptune", "Uranus"],
                "answer": "Jupiter",
            },
        ]

    if "photosynth" in t or "plant" in t:
        return [
            {
                "question": "What do plants need for photosynthesis?",
                "options": [
                    "Sunlight, water and carbon dioxide",
                    "Oxygen, sugar and water",
                    "Nitrogen, hydrogen and helium",
                    "Only water and soil",
                ],
                "answer": "Sunlight, water and carbon dioxide",
            },
            {
                "question": "Which gas do plants release during photosynthesis?",
                "options": ["Carbon dioxide", "Nitrogen", "Oxygen", "Hydrogen"],
                "answer": "Oxygen",
            },
            {
                "question": "Where does photosynthesis mainly occur in a plant?",
                "options": ["Roots", "Stem", "Leaves", "Flowers"],
                "answer": "Leaves",
            },
        ]

    return [
        {
            "question": "What best describes '" + topic + "'?",
            "options": [
                "The core principles and ideas of " + topic,
                "An unrelated cooking technique",
                "A brand of mobile phone",
                "A musical instrument",
            ],
            "answer": "The core principles and ideas of " + topic,
        },
        {
            "question": "Why is studying '" + topic + "' useful?",
            "options": [
                "It has no practical use",
                "It builds foundational knowledge in this field",
                "It is only for professors",
                "It was invented yesterday",
            ],
            "answer": "It builds foundational knowledge in this field",
        },
        {
            "question": "What is the best way to master '" + topic + "'?",
            "options": [
                "Never study it",
                "Read it once and forget",
                "Learn concepts, practise examples and self test",
                "Memorise without understanding",
            ],
            "answer": "Learn concepts, practise examples and self test",
        },
    ]


def generate_quiz(text):
    text = (text or "").strip()
    if not text:
        return [{"error": "Please provide a topic or passage for the quiz."}]

    if not is_demo():
        prompt = (
            "You are a quiz generator for students.\n"
            "Create exactly 3 multiple choice questions about:\n" + text + "\n\n"
            "Each question must have exactly 4 options and one correct answer that "
            "matches one option exactly, character for character.\n"
            "Return ONLY a raw JSON array. No markdown and no explanation.\n"
            'Format: [{"question":"...","options":["A","B","C","D"],"answer":"A"}]'
        )
        raw = generate_text(prompt, temperature=0.8, max_tokens=1500)
        if raw:
            try:
                parsed = json.loads(clean_json_block(raw))
                valid = _validate(parsed)
                if valid:
                    return valid[:3]
            except Exception as exc:
                print("[EduGenie] Quiz parse issue:", exc)

    return _demo_quiz(text)