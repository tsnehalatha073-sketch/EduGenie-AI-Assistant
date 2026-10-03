from config import generate_text, is_demo

DEMO_EXPLANATIONS = {
    "photosynthesis": "Photosynthesis is how plants make their own food. Leaves absorb sunlight, roots absorb water, and tiny pores take in carbon dioxide from the air. Using the Sun's energy, the plant combines water and carbon dioxide into glucose and releases oxygen. Example: a mango tree in your garden is quietly producing sugar and the oxygen you breathe.",
    "gravity": "Gravity is an invisible pulling force between objects that have mass. The heavier the object, the stronger its pull. Earth's gravity keeps your feet on the ground and makes a dropped pen fall. The same force keeps the Moon circling Earth and Earth circling the Sun.",
    "binary search": "Binary Search finds an item in a sorted list very quickly. Look at the middle item. If your target is smaller, search only the left half. If it is bigger, search only the right half. Repeat until found. Example: finding a word in a dictionary, you open the middle, not page one.",
    "quantum computing": "Quantum computing uses the rules of quantum physics to compute. Normal computers use bits that are either 0 or 1. Quantum computers use qubits that can be 0 and 1 at the same time, called superposition. This lets them explore many possibilities at once and solve certain problems far faster.",
    "machine learning": "Machine Learning lets a computer learn from examples instead of fixed rules. Show it thousands of labelled cat and dog photos and it discovers the patterns itself. Later it can look at a brand new photo and say that is a dog. This is how spam filters and recommendations work.",
    "recursion": "Recursion is when a function calls itself to solve a smaller version of the same problem. It needs a base case to stop. Example: to find 5 factorial you calculate 5 times 4 factorial, then 4 times 3 factorial, and so on until you reach 1.",
}


def explain_topic(topic):
    topic = (topic or "").strip()
    if not topic:
        return "Please provide a topic to explain."

    if not is_demo():
        prompt = (
            "Explain the concept of '" + topic + "' to a school student.\n"
            "Rules: simple everyday language, under 150 words, no jargon, "
            "and finish with one short real world example.\n"
            "Write plain flowing text, not bullet points."
        )
        result = generate_text(prompt, temperature=0.6, max_tokens=600)
        if result:
            return result

    lowered = topic.lower()
    for key in DEMO_EXPLANATIONS:
        if key in lowered:
            return DEMO_EXPLANATIONS[key] + "\n\n[Demo Mode - add GOOGLE_API_KEY in .env for live AI explanations]"

    return (
        topic + " is an important concept worth learning step by step.\n\n"
        "1. Definition - find out exactly what " + topic + " means\n"
        "2. Example - look for a real world example of " + topic + "\n"
        "3. Practice - solve three to five questions on " + topic + "\n"
        "4. Connect - link " + topic + " to topics you already know\n\n"
        "[Demo Mode - add GOOGLE_API_KEY in .env for live AI explanations]"
    )