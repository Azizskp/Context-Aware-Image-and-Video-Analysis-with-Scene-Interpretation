from openai import OpenAI

# 🔑 Your DeepSeek API key
client = OpenAI(
    api_key= "YOUR_API_KEY",
    base_url="https://api.deepseek.com"
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

        response = client.chat.completions.create(
            model="deepseek/deepseek-v4-flash:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    except Exception as e:

        print("DeepSeek Error:", e)

        return "AI scene interpretation unavailable"