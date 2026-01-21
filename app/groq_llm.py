import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = None

if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
else:
    print("Warning: GROQ_API_KEY not found. LLM calls will fail.")

def generate_answer(prompt: str, max_tokens: int = 512, temp: float = 0.1):
    """
    Generates an answer using Groq's llama3-8b-8192 model.
    Includes basic retry logic for rate limits.
    """
    if not client:
        return "Error: API Key missing."

    model_name = "llama-3.3-70b-versatile"
    retries = 3
    
    for attempt in range(retries):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=model_name,
                max_tokens=max_tokens,
                temperature=temp,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            error_msg = str(e).lower()
            if "rate limit" in error_msg or "429" in error_msg:
                wait_time = 2 * (attempt + 1)
                print(f"Rate limit hit. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Error generating answer: {e}")
                return f"I'm sorry, I encountered an error: {str(e)}"
    
    return "I am currently experiencing high traffic. Please try again in a moment."

if __name__ == "__main__":
    if GROQ_API_KEY:
        print(generate_answer("Say hello"))
    else:
        print("Set GROQ_API_KEY to test.")
