from config import generate_text, is_demo

DEMO_KB = {
    "largest ocean": "The Pacific Ocean is the largest ocean on Earth. It covers about 165 million square kilometres, which is more than all of Earth's land area combined.",
    "sky blue": "The sky looks blue because of Rayleigh scattering. Sunlight contains all colours, and blue light has a shorter wavelength, so air molecules scatter it much more than red or yellow light.",
    "pythagoras": "The Pythagorean Theorem says that in a right angled triangle, a squared plus b squared equals c squared, where c is the hypotenuse (the longest side).",
    "photosynthesis": "Photosynthesis is the process where green plants use sunlight, water and carbon dioxide to make glucose and release oxygen.",
    "gravity": "Gravity is the force that attracts objects with mass toward each other. It keeps us on the ground and keeps planets orbiting the Sun.",
    "solar system": "Our Solar System contains the Sun and eight planets: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus and Neptune.",
    "dna": "DNA stores the genetic instructions of living organisms. It has a double helix shape built from the bases A, T, G and C.",
    "water cycle": "The water cycle is the continuous movement of water through evaporation, condensation, precipitation and collection.",
    "newton": "Newton's three laws describe motion. First, objects stay at rest or in motion unless a force acts. Second, force equals mass times acceleration. Third, every action has an equal and opposite reaction.",
}


def answer_question(question):
    question = (question or "").strip()
    if not question:
        return "Please ask a valid question."

    if not is_demo():
        prompt = (
            "You are EduGenie, a friendly AI tutor for students.\n"
            "Answer the question clearly, accurately and concisely in under 180 words.\n"
            "Use simple language and add a short example if it helps.\n\n"
            "Question: " + question
        )
        result = generate_text(prompt, temperature=0.4, max_tokens=800)
        if result:
            return result

    lowered = question.lower()
    for key in DEMO_KB:
        if key in lowered:
            return DEMO_KB[key] + "\n\n[Demo Mode - add GOOGLE_API_KEY in .env for live Gemini answers]"

    return (
        "You asked: " + question + "\n\n"
        "With a valid Gemini API key, EduGenie answers this instantly using gemini-2.5-flash.\n\n"
        "[Demo Mode - add GOOGLE_API_KEY in .env to enable live AI]"
    )