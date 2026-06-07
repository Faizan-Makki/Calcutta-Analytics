from openai import OpenAI
from apiconfig import api_key, api_key2

def ai_help(prompt):
    try:
        client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message.content
        return result

    except Exception as e:
        try:
            client = OpenAI(
            api_key=api_key2,
            base_url="https://api.groq.com/openai/v1")
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content
            return result
        except Exception as e2:
            return f"API 1 & 2 both Failed, Error1: {e} Error2: {e2}"
