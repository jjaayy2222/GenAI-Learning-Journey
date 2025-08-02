import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def basic_chat(user_input):
    """간단한 대화 함수"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200,                             
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"오류 발생: {str(e)}"

# 사용 예시
if __name__ == "__main__":
    user_question = "Python에서 리스트와 튜플의 차이점은?"
    answer = basic_chat(user_question)
    print(f"질문: {user_question}")
    print(f"답변: {answer}")


    """
    - 셀 출력 : max_tokens=200
        질문: Python에서 리스트와 튜플의 차이점은?
        답변: 파이썬에서 리스트와 튜플은 모두 데이터의 집합을 저장하는 데 사용되지만, 몇 가지 중요한 차이점이 있습니다.

        1. **변경 가능성 (Mutability)**:
        **리스트 (list)**: 변경 가능합니다. 즉, 리스트의 요소를 추가, 삭제 또는 변경할 수 있습니다.
        ```python
            my_list = [1, 2, 3]
            my_list[0] = 10  # 변경 가능
            my_list.append(4)  # 요소 추가
        ```
        **튜플 (tuple)**: 변경 불가능합니다. 즉, 한 번 생성된 튜플의 요소는 변경할 수 없습니다.
        ```python
        my_tuple = (1, 2, 3)
        # my_tuple[0] = 10  # 오류 발생: 'tuple' object does not support item assignment
        ```

        2. **생성 방법**
        ------------------- 
        
            ㄴ 여기에서 출력이 끊김
    
    - 문제점 : max_tokens이 낮아 출력이 끊김 → 높여서 답의 차이를 확인 `06_baic_chat_increased_max_tokens.py`
    
    """