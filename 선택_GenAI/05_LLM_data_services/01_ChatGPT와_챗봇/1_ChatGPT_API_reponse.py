import os                                                      
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_response(prompt: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    msg = resp.choices[0].message.content                               # 응답으로부터 메시지를 추출
    return msg


if __name__ == "__main__":
    prompt = input("You: ")
    response = get_response(prompt)
    print(f"AI:", response)
    
    
"""
You: 안녕
AI: 안녕하세요! 어떻게 도와드릴까요?
"""    