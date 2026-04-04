import requests

def call_llm(user_input, memory):

    prompt = f"""
You are an intelligent AI tutor.

User previous messages:
{memory}

Current question:
{user_input}

Instructions:
- Adapt your answer based on user history
- Be clear and educational
- Avoid unnecessary repetition

Answer:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]