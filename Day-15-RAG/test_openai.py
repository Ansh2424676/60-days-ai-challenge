import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")

print("Key found:", bool(api_key))
print("Key prefix:", api_key[:8] if api_key else "None")

client = OpenAI(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="gpt-5.6-luna",
        messages=[
            {
                "role": "user",
                "content": "Say hello in one short sentence."
            }
        ]
    )

    print("\nAPI TEST SUCCESS")
    print(response.choices[0].message.content)

except Exception as e:
    print("\nAPI TEST FAILED")
    print(type(e).__name__)
    print(e)