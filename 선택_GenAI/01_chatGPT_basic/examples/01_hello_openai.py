# 01_chatGPT_basic/examples/hello_openai.py

import os                                                       # 활성화되지 않을 경우 명령팔레트에서 파이썬 인터프리터 경로 올바르게 설정하기
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello, OpenAI!"}],
        max_tokens=50
    )
    
    print("🎉 성공!", response.choices[0].message.content)
    print("사용 토큰:", response.usage.total_tokens)
    
except Exception as e:
    print("❌ 오류:", str(e))

    """
    - 셀 출력 : 
        - 🎉 성공! Hello! How can I assist you today?
        - 사용 토큰: 21
    """