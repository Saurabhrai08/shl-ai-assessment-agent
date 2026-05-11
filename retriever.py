import json

# Load dataset
with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


def retrieve_assessments(query):

    query = query.lower()

    scored = []

    # Important keywords
    important_keywords = [
        "java",
        "python",
        "developer",
        "software",
        "programming",
        "coding",
        "communication",
        "teamwork",
        "personality",
        "sales",
        "customer service"
    ]

    for item in catalog:

        text = (
            item.get("name", "") + " " +
            item.get("description", "") + " " +
            " ".join(item.get("keys", []))
        ).lower()

        score = 0

        # Strong keyword matching
        for keyword in important_keywords:

            if keyword in query and keyword in text:

                # Technical keywords get higher weight
                if keyword in [
                    "java",
                    "python",
                    "developer",
                    "programming",
                    "coding",
                    "software"
                ]:
                    score += 5

                else:
                    score += 2

        # Basic word overlap
        for word in query.split():

            if word in text:
                score += 1

        if score > 0:
            scored.append((score, item))

    # Sort descending
    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [x[1] for x in scored[:10]]