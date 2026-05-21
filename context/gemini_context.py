from google import genai

# 🔑 Your API key here
client = genai.Client(
    api_key= "YOUR_API_KEY"
)


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

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:

        print("Gemini Error:", e)

        return "AI scene interpretation unavailable"