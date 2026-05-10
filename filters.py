def filter_results(results, query):

    query = query.lower()

    scored_results = []

    communication_needed = any(
        word in query
        for word in [
            "communication",
            "teamwork",
            "stakeholder",
            "collaboration"
        ]
    )

    for item in results:

        text = (
            item.get("name", "") + " " +
            item.get("description", "") + " " +
            " ".join(item.get("keys", []))
        ).lower()

        score = 0

        # -----------------------------
        # Java / Technical Matching
        # -----------------------------

        tech_keywords = [
            "java",
            "developer",
            "programming",
            "coding",
            "software"
        ]

        for word in tech_keywords:
            if word in query and word in text:
                score += 3

        # -----------------------------
        # Communication / Behavioral
        # -----------------------------

        if communication_needed:

            communication_keywords = [
                "communication",
                "teamwork",
                "collaboration",
                "stakeholder"
            ]

            for word in communication_keywords:
                if word in text:
                    score += 4

            # Boost personality assessments
            if "Personality & Behavior" in item.get("keys", []):
                score += 5

        # -----------------------------
        # Keep useful results
        # -----------------------------

        if score > 0:
            scored_results.append((score, item))

    # Sort descending
    scored_results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [x[1] for x in scored_results]
