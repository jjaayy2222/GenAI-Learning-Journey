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
            max_tokens=1000,                             # 초기 max_tokens=200 → 1000로 답의 차이를 확인 
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
    - 셀 출력 : max_tokens=1000 → 성공
        질문: Python에서 리스트와 튜플의 차이점은?
        답변: Python에서 리스트와 튜플은 모두 여러 값을 저장할 수 있는 자료구조이지만, 몇 가지 중요한 차이점이 있습니다.

        1. **변경 가능성 (Mutability)**:
        - **리스트**: 변경 가능합니다. 즉, 리스트의 요소를 추가, 삭제, 변경할 수 있습니다.
            ```python
            my_list = [1, 2, 3]
            my_list[0] = 10  # 리스트의 첫 번째 요소를 변경
            my_list.append(4)  # 요소 추가
            print(my_list)  # 출력: [10, 2, 3, 4]
            ```
        - **튜플**: 변경 불가능합니다. 즉, 한 번 생성된 튜플의 요소는 변경할 수 없습니다.
            ```python
            my_tuple = (1, 2, 3)
            # my_tuple[0] = 10  # 오류 발생: 'tuple' object does not support item assignment
            ```

        2. **구조**:
        - **리스트**: 대괄호 `[]`로 생성합니다.
            ```python
            my_list = [1, 2, 3]
            ```
        - **튜플**: 괄호 `()`로 생성합니다.
            ```python
            my_tuple = (1, 2, 3)
            ```
        - 튜플을 생성할 때 한 개의 요소만 포함하는 경우에는 쉼표를 반드시 붙여야 합니다.
            ```python
            single_element_tuple = (1,)  # 튜플
            ```

        3. **성능**:
        - 튜플은 리스트보다 메모리 사용이 적고, 생성 속도가 더 빠릅니다. 따라서 불변의 데이터를 저장할 때 튜플을 사용하는 것이 더 효율적일 수 있습니다.

        4. **사용 용도**:
        - **리스트**: 변경 가능한 데이터의 집합을 다룰 때 사용합니다. 예를 들어, 데이터를 추가하거나 삭제해야 하는 경우.
        - **튜플**: 변하지 않는 데이터의 집합을 다룰 때 사용합니다. 예를 들어, 함수의 반환값으로 여러 값을 함께 반환할 때 튜플을 사용할 수 있습니다.

        이러한 차이점들을 고려하여 상황에 맞게 리스트와 튜플을 선택하여 사용하면 됩니다.
    
    ----------------------------------------------------------------------------------------------------
    
    - (비교) 셀 출력 : max_tokens=200
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
        
    """