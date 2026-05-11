from fastapi import FastAPI
from pydantic import BaseModel

from retriever import retrieve_assessments
from conversation import detect_intent
from filters import filter_results
from comparison import compare_assessments
from llm import generate_reply

app = FastAPI()


# -----------------------------
# Schemas
# -----------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


# -----------------------------
# Root Endpoint
# -----------------------------

@app.get("/")
def root():
    return {
        "message": "SHL AI Assessment Recommendation API is running"
    }


# -----------------------------
# Health Endpoint
# -----------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------
# Chat Endpoint
# -----------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    # Convert messages
    messages = [m.dict() for m in request.messages]

    # -----------------------------
    # Combine conversation context
    # -----------------------------

    conversation_context = " ".join(
        [
            m["content"]
            for m in messages
            if m["role"] == "user"
        ]
    )

    # -----------------------------
    # Off-topic refusal
    # -----------------------------

    blocked_topics = [
        "weather",
        "politics",
        "medical",
        "legal",
        "stock market",
        "movie",
        "sports"
    ]

    if any(
        topic in conversation_context.lower()
        for topic in blocked_topics
    ):

        return {
            "reply": (
                "I can only assist with "
                "SHL assessment recommendations."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # Detect intent
    # -----------------------------

    intent = detect_intent(messages)

    # -----------------------------
    # Clarification handling
    # -----------------------------

    if intent == "clarification":

        return {
            "reply": (
                "Could you specify the role, "
                "experience level, and required skills?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # Retrieve assessments
    # -----------------------------

    results = retrieve_assessments(
        conversation_context
    )

    # -----------------------------
    # Apply filtering/reranking
    # -----------------------------

    results = filter_results(
        results,
        conversation_context
    )

    # -----------------------------
    # Comparison mode
    # -----------------------------

    if intent == "comparison":

        comparison_text = compare_assessments(
            results
        )

        return {
            "reply": comparison_text,
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # Build recommendations
    # -----------------------------

    recommendations = []

    for item in results[:5]:

        test_type = (
            item["keys"][0]
            if item.get("keys")
            else "Assessment"
        )

        recommendations.append({
            "name": item["name"],
            "url": item["link"],
            "test_type": test_type
        })

    # -----------------------------
    # Generate conversational reply
    # -----------------------------

    reply_text = generate_reply(
        conversation_context,
        results[:5]
    )

    # -----------------------------
    # Final response
    # -----------------------------

    return {
        "reply": reply_text,
        "recommendations": recommendations,
        "end_of_conversation": False
    }