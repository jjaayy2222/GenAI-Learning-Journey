import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def test_prompts():
    """다양한 프롬프트 실험"""
    prompts = [
        "좋은 하루 보내세요!",
        "이번 주 날씨 어때요?",
        "Python에서 리스트와 딕셔너리 차이는?",
        "생산성 향상 팁 3가지 알려줘"
    ]

    for i, prompt in enumerate(prompts):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )
            print(f"[{i+1}] 프롬프트: {prompt}")
            print("응답:", response.choices[0].message.content)
            print("---")
        except Exception as e:
            print(f"오류 발생 [{i+1}]:", str(e))

if __name__ == "__main__":
    test_prompts()


    """
    
    - 셀 출력
        [1] 프롬프트: 좋은 하루 보내세요!
        응답: 좋은 하루 보내세요! 궁금한 점이나 도움이 필요한 부분이 있다면 언제든지 말씀해 주세요.
        ---
        [2] 프롬프트: 이번 주 날씨 어때요?
        응답: 죄송하지만, 실시간 정보나 최신 날씨 데이터를 제공할 수는 없습니다. 그러나 지역의 기상청 웹사이트나 날씨 앱을 통해 이번 주 날씨를 확인하실 수 있습니다. 필요한 다른 정보가 있다면 말씀해 주세요!
        ---
        [3] 프롬프트: Python에서 리스트와 딕셔너리 차이는?
        응답: Python에서 리스트(list)와 딕셔너리(dictionary)는 두 가지 중요한 데이터 구조로, 각기 다른 용도와 특징을 가지고 있습니다.

        ### 리스트 (List)

        - **정의**: 리스트는 순서가 있는 변경 가능(mutable)한 컬렉션으로, 다양한 데이터 타입의 요소들을 저장할 수 있습니다.
        - **형태**: 대괄호 `[]`를 사용하여 생성합니다.
        - **인덱스**: 리스트의 각
        ---
        [4] 프롬프트: 생산성 향상 팁 3가지 알려줘
        응답: 생산성을 향상시키기 위한 팁 3가지를 소개합니다:

        1. **우선순위 설정하기**: 하루의 업무를 시작하기 전에 중요한 업무와 긴급한 업무를 구분해 우선순위를 매기세요. '아이젠하워 매트릭스'와 같은 도구를 활용하여 어떤 일이 가장 중요한지 파악하고, 이에 집중하는 것이 좋습니다. 

        2. **작업 시간 블록 설정하기**:
        ---
        
        ㄴ 여기에서 출력이 끊김
        
    - 스크립트에서 날씨 조건을 "서울"로 구체적으로 수정하고, 가져올 수 없다면 기상청이나 다른 곳을 참고할 수 있도록 조건문을 추가하기로 함 → `05_prompt_test_weather_prompt.py`

    """