def generate_reply(user_query, recommendations):

    if not recommendations:
        return "I could not find suitable SHL assessments."

    names = []

    for item in recommendations:
        names.append(item["name"])

    recommendation_list = ", ".join(names)

    return (
        f"Based on your hiring requirements, "
        f"the following SHL assessments are recommended: "
        f"{recommendation_list}."
    )