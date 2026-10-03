from config import generate_text, is_demo


def _demo_path(topic):
    return (
        topic + " Learning Path: From Zero to Hero\n\n"
        "This path introduces " + topic + " progressively from basics to advanced. "
        "It is adaptive, so adjust the pace to your own level.\n\n"

        "I. BEGINNER LEVEL - Building a Foundation\n"
        "Estimated Time: 1 to 2 weeks\n\n"
        "Key Topics:\n"
        "- What is " + topic + "? Overview, history and why it matters\n"
        "- Core terminology and fundamental concepts\n"
        "- Setting up your environment and first steps\n"
        "- Simple guided examples and daily exercises\n\n"
        "Resources:\n"
        "- Interactive: Khan Academy, Codecademy, W3Schools\n"
        "- Videos: freeCodeCamp on YouTube, CrashCourse\n"
        "- Practice: 20 to 30 minutes of exercises every day\n\n"

        "II. INTERMEDIATE LEVEL - Building Real Skills\n"
        "Estimated Time: 2 to 3 weeks\n\n"
        "Key Topics:\n"
        "- Advanced concepts and common techniques\n"
        "- Working with real world data and examples\n"
        "- Design patterns and best practices\n"
        "- Build two or three small projects end to end\n\n"
        "Resources:\n"
        "- Books: well rated beginner to intermediate books on " + topic + "\n"
        "- Courses: Coursera, Udemy, edX specialisations\n"
        "- Practice: LeetCode, HackerRank, Kaggle challenges\n\n"

        "III. ADVANCED LEVEL - Mastery\n"
        "Estimated Time: 3 to 4 weeks and beyond\n\n"
        "Key Topics:\n"
        "- Internals, architecture and expert level concepts\n"
        "- Performance optimisation and debugging\n"
        "- Industry standards and production best practices\n"
        "- Open source contribution and teaching others\n\n"
        "Resources:\n"
        "- Official documentation and advanced specialised books\n"
        "- Communities: forums, Discord, Reddit, local meetups\n"
        "- Build one portfolio grade capstone project\n\n"

        "ADAPTIVE LEARNING TIPS:\n"
        "- Start with the basics and never rush into advanced topics\n"
        "- Practise regularly, consistency beats long rare sessions\n"
        "- Use real world datasets and scenarios\n"
        "- Focus on understanding, not memorising\n"
        "- Break complex problems into smaller parts\n"
        "- Experiment and compare different approaches\n"
        "- Ask for help in communities when you get stuck\n\n"

        "This gives you a solid roadmap to master " + topic + ". Adapt it to your goals.\n\n"
        "[Demo Mode - add GOOGLE_API_KEY in .env for a personalised Gemini learning path]"
    )


def get_learning_recommendations(topic):
    topic = (topic or "").strip()
    if not topic:
        return "Please provide a topic to get learning recommendations."

    if not is_demo():
        prompt = (
            "You are an expert AI tutor. A student wants to learn: " + topic + ".\n\n"
            "Create a structured adaptive learning path with:\n"
            "1. Beginner, Intermediate and Advanced levels\n"
            "2. Key topics in the correct learning order for each level\n"
            "3. Estimated time for each level\n"
            "4. Specific real resources such as books, YouTube channels, courses and websites\n"
            "5. A final section of adaptive learning tips\n\n"
            "Use clear headings and plain text. Do not use markdown tables."
        )
        result = generate_text(prompt, temperature=0.7, max_tokens=3000)
        if result:
            return result

    return _demo_path(topic)