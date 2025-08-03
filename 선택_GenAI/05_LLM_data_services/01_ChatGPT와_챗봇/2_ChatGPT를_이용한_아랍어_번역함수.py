import os                                                      
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 번역할 예시 문장
ARABIC_TEXT = "الأفضل!"

def ara_to_kor(arabic_text: str) -> str:
    chat_log = [
        {
            "role":"system",
            "content":"너는 아랍어를 한국어로 번역하는 챗봇이야. 번역문 앞뒤에 설명은 생략하고 한국어로 번역한 결과만 반환해."
        }
    ]

    chat_log.append({"role": "user", "content": arabic_text})

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=chat_log,
    )
    
    msg = resp.choices[0].message.content                               # 응답으로부터 메시지를 추출

    return msg


if __name__ == "__main__":
    print("아랍어:", ARABIC_TEXT)
    korean_text = ara_to_kor(ARABIC_TEXT)
    print("한국어:", korean_text)


"""
    아랍어: الأفضل! 
    한국어:최고!
"""