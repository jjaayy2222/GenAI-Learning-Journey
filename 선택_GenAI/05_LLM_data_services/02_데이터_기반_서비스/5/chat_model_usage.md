# 대화형 모델 사용법 (`chat model`)

## 1. 대화를 계속 이어가려면?
`chat.complitions` 의 **`messages`** 통해 관리!! 

- 대화를 지속적으로 이어가기 위해선, 이전 메시지를 `messages 배열`에 쌓아가며 계속해서 `API`를 호출
  
- 예시

    ```

        import openai

        # 대화 상태 초기화 (사용자와 AI의 첫 대화)
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},          # 시스템 메시지
            {"role": "user", "content": "안녕, 오늘 날씨 어때?"}                        # 사용자 메시지
        ]

        # 대화를 계속하기 위한 함수
        def chat_with_gpt(messages):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages                                                   # 이전 메시지들을 계속 포함
            )
            return response['choices'][0]['message']['content']

        # 첫 번째 대화
        response = chat_with_gpt(messages)
        print(response)                                                             # AI의 첫 번째 응답

        # 대화 상태 업데이트: 새로운 사용자의 질문 추가
        messages.append({"role": "user", "content": "내일 날씨는?"})

        # 두 번째 대화
        response = chat_with_gpt(messages)
        print(response)                                                             # AI의 두 번째 응답

    ```

- `messages.append` = **user와 assistant**의 메시지 → 모델은 이전 메시지들을 기억하고 대화를 이어감

- `system 메시지` = 모델의 행동 설정하는 역할
  - 예시: "You are a helpful assistant" = 모델에게 친절하고 유용한 답변을 하도록 지시함


## 2. 대화의 흐름을 관리하려면?

- 대화 길이에 따라 이전 메시지를 적절히 다룰 필요 있음 → 너무 많은 메시지를 보내면 토큰 제한을 초과할 수 있기 때문

- 최근 몇 개의 메시지만 보내거나 요약된 형태로 보내는 방법 고려해볼 수 있음

    ```

        # 너무 긴 대화에서 최근 몇 개 메시지만 사용할 수 있도록 필터링
        MAX_TOKENS = 1000                                                      # 예시로 설정한 최대 토큰 수

        def trim_messages(messages):
            # 이곳에서 길이를 잘라낼 수 있음 (예: 가장 최근 5개 메시지만 남기기)
            return messages[-5:]

        # 대화 업데이트 시, 대화가 길어지면 메시지 수를 조절
        messages = trim_messages(messages)
        response = chat_with_gpt(messages)

    ```


## 3. `chat_completions` 사용 시 주의사항

- 대화가 길어질수록 **응답 시간**이 길어질 수 있음
  
- **토큰 수 제한(`최대 4096 tokens`)** = `모델이 한 번에 처리할 수 있는 내용의 양 결정` → 이 한도를 넘지 않도록 대화 관리
  
  - `GPT-4 모델`의 토큰 한도 예시:
    - `GPT-4 (4k-tokens)` : 최대 `4096 토큰`
    - `GPT-4 (8k-tokens)`: 최대 `8192 토큰`
    - `GPT-4 (32k-tokens)`: 최대 `32,768 토큰`

  - 토큰 수 계산 예시:
    - `1 토큰` = 대체로 `영어 단어 한 개` or `공백을 포함한 한 글자`로 계산
    - 예시: "Hello, world!" = 4개의 토큰
 

## 4. **`utls.py`** 수정 or 재작성 

- Function Calling이 아닌 대화형 모델에서는 `대화의 맥락`을 `유지`하는 방식으로 작동


### 1) 기존 `utils.py` 와의 차이점

- 대화 메시지와 관련된 형식(`messages`, `role`, `content`)이 필요 → **대화형 메시지의 구조 필요**

    ```

        def message_to_json_schema(role: str, content: str) -> dict:
            """Converts a message into the format expected by the OpenAI chat model."""
            return {
                "role": role,                                               # 'system', 'user', or 'assistant'
                "content": content                                          # The actual message content
            }

        def create_chat_messages(user_message: str) -> list:
            """Creates a series of messages for OpenAI's Chat API."""
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},           # System-level context
                {"role": "user", "content": user_message},  # User's input message
            ]
            return messages

    ```

- **대화형 모델 스키마 구조**
  
  - `role` = 메시지를 보낸 `주체` (예: `user`, `assistant`, `system`)
  - `content` = 메시지 `내용`
    - 대화 예시
      - 사용자: "안녕, 오늘 날씨 어때?"
      - 모델: "오늘은 맑고 기온은 25도입니다."
  - `messages` = 대화의 흐름을 이어가는 데 사용되는 메시지 `배열`

        ```

            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "안녕, 오늘 날씨 어때?"},
                {"role": "assistant", "content": "오늘은 맑고 기온은 25도입니다."},
            ]

        ```

### 2) 대화형 모델을 위한 `utils.py` 업데이트

- 예시로 수정한 코드
  
    ```
        def message_to_json_schema(role: str, content: str) -> dict:
            """대화형 모델에 맞는 메시지 형식으로 변환"""
            return {
                "role": role,    # 'user', 'assistant', 'system'
                "content": content  # 메시지 내용
            }

        def create_chat_messages(user_message: str) -> list:
            """대화형 모델에서 사용할 수 있도록 메시지 배열 생성"""
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},                 
                                                                                        # 시스템 메시지
                {"role": "user", "content": user_message},
                                                                                        # 사용자의 메시지
            ]
            return messages

        def update_conversation(messages: list, new_message: str) -> list:
            """이전 대화 내역을 업데이트하며 새로운 메시지 추가"""
            messages.append({"role": "user", "content": new_message})
            return messages

    ```

<br>

- 대화형 모델을 위한 코드 흐름
    - `messages 배열`을 `생성`하고, 초기 system 메시지로 시작
    - `사용자 입력`에 따라 `user 메시지`를 추가하고, `OpenAI API`에 `전달`
    - `모델의 응답`은 `assistant 역할`로 기록
    - 새로운 `대화`가 `추가`될 때마다 `messages`에 `user 메시지`를 `추가` → 계속해서 대화가 이어짐<br><br>

- 대화형 모델에서 `utils.py` 의 역할
    - 대화 모델을 위한 메시지 배열 구성
    - 대화 상태 관리


