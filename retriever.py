import json

# Load dataset
with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


def retrieve_assessments(query):

    query = query.lower()

    scored = []

    for item in catalog:

        text = (
            item.get("name", "") + " " +
            item.get("description", "") + " " +
            " ".join(item.get("keys", []))
        ).lower()

        score = 0

        for word in query.split():

            if word in text:
                score += 1

        if score > 0:
            scored.append((score, item))

    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [x[1] for x in scored[:10]]