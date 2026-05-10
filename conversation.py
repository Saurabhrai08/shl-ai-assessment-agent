def detect_intent(messages):

    latest = messages[-1]["content"].lower()

    comparison_words = [
        "compare",
        "difference",
        "vs",
        "versus"
    ]

    for word in comparison_words:
        if word in latest:
            return "comparison"

    vague_phrases = [
        "need assessment",
        "need test",
        "hiring",
        "assessment"
    ]

    if any(p in latest for p in vague_phrases):
        if len(latest.split()) < 6:
            return "clarification"

    return "recommendation"