import re
from config import generate_text, is_demo


def summarize_text(text):
    text = (text or "").strip()
    if not text:
        return "Please provide text to summarize."
    if len(text) < 25:
        return "Text is too short to summarize. Please paste a longer passage."

    if not is_demo():
        prompt = (
            "Summarize the following passage for a student.\n"
            "Rules: simple language, keep every key fact, remove repetition, "
            "aim for about 25 percent of the original length.\n\n"
            "Passage:\n" + text
        )
        result = generate_text(prompt, temperature=0.3, max_tokens=1200)
        if result:
            return result

    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

    if len(sentences) <= 2:
        return text + "\n\n[Demo Mode - add GOOGLE_API_KEY in .env for AI summarization]"

    picked = [sentences[0]]
    middle = sentences[len(sentences) // 2]
    if middle not in picked:
        picked.append(middle)
    if sentences[-1] not in picked:
        picked.append(sentences[-1])

    return (
        " ".join(picked)
        + "\n\nOriginal: " + str(len(text)) + " characters / " + str(len(sentences)) + " sentences"
        + "\n[Demo Mode - add GOOGLE_API_KEY in .env for AI summarization]"
    )