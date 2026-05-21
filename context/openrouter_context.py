import requests
import json

# 🔑 Your OpenRouter API Key
OPENROUTER_API_KEY = "YOUR_API_KEY"


def generate_scene_description(objects):

    prompt = f"""
Detected objects:
{objects}

Describe the real-world scene naturally.

Examples:
- Heavy traffic on a busy road
- Person walking a dog
- People dining in a restaurant

Keep answer under 12 words.
"""

    try:

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",

            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },

            data=json.dumps({
                "model": "openai/gpt-4o-mini",

                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:

        print("OpenRouter Error:", e)

        return "AI scene interpretation unavailable"