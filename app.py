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

    return {
        "status": "ok"
    }


# -----------------------------
# Chat Endpoint
# -----------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    # -----------------------------
    # Convert messages
    # -----------------------------

    messages = [m.dict() for m in request.messages]

    # -----------------------------
    # Turn limit protection
    # -----------------------------

    if len(messages) >= 8:

        return {
            "reply": (
                "Conversation limit reached. "
                "Please start a new request."
            ),
            "recommendations": [],
            "end_of_conversation": True
        }

    # -----------------------------
    # Build conversation context
    # -----------------------------

    conversation_context = " ".join(
        [
            m["content"]
            for m in messages
            if m["role"] == "user"
        ]
    )

    conversation_context_lower = (
        conversation_context.lower()
    )

    # -----------------------------
    # Off-topic + injection refusal
    # -----------------------------

    blocked_topics = [
        "weather",
        "politics",
        "medical",
        "legal",
        "stock market",
        "movie",
        "sports",

        # Prompt injection attempts
        "ignore previous instructions",
        "ignore all instructions",
        "system prompt",
        "reveal prompt",
        "show hidden prompt",
        "bypass",
        "jailbreak",
        "developer message",
        "internal instructions",
        "override instructions"
    ]

    if any(
        topic in conversation_context_lower
        for topic in blocked_topics
    ):

        return {
            "reply": (
                "I can only assist with SHL assessment "
                "recommendations and cannot follow "
                "unrelated or unsafe instructions."
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

    filtered_results = filter_results(
        results,
        conversation_context
    )

    if filtered_results:
        results = filtered_results

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
        "end_of_conversation": True
    }