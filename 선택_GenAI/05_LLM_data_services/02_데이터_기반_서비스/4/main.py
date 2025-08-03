# main.py

import os
import sys
import json
from dotenv import load_dotenv
from db import query_db
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage

# 터미널에서 한글 입력 가능하도록 인코딩 설정
sys.stdin.reconfigure(encoding="utf-8")

# .env 파일 로드 (루트에 있는 환경변수 로드됨)
load_dotenv()

# OpenAI API 클라이언트 초기화 (.env에서 키 가져옴)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# DB 스키마 설명 파일 읽기 (모델이 테이블 구조를 이해하기 위해 사용)
with open("DB_SCHEMA.txt", "rt", encoding="utf-8") as f:
    DB_SCHEMA = f.read()

# GPT가 호출할 함수 정의 (query_db)
query_db_info = {
    "name": "query_db",
    "description": "데이터베이스에 쿼리를 실행하고 결과를 반환합니다.\n\n" + DB_SCHEMA,
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "호출할 SQL 쿼리 문자열",
            }
        },
        "required": ["query"],
        "additionalProperties": False,
    },
}

# 실제 GPT 응답 처리
def get_response(chat_log: list, tools: dict = None) -> ChatCompletionMessage:
    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=chat_log, 
        tools=tools,
        tool_choice="auto",
    )

    if response.choices[0].message.tool_calls:
        tool_call_results = []
        for tool_call in response.choices[0].message.tool_calls:
            call_id = tool_call.id

            if tool_call.function.name == "query_db":
                query_str = json.loads(tool_call.function.arguments)["query"]
                result = query_db(query_str)

                call_result_message = {
                    "tool_call_id": call_id,
                    "role": "tool",
                    "content": json.dumps(
                        {"result": str(result)},
                        ensure_ascii=False,
                    ),
                }
                tool_call_results.append(call_result_message)

        # ✅ messages → chat_log에 반영해줘야 함!
        chat_log += [response.choices[0].message] + tool_call_results   # ⭐ 이거 꼭 필요함

        # 재요청 시 messages 대신 chat_log 사용
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=chat_log, tools=tools
        )

    return response.choices[0].message

def main():
    tools = [
        {
            "type": "function",
            "function": query_db_info,
        }
    ]

    chat_log = [
        {
            "role": "system",
            "content": "너는 유용한 고객 지원 어시스턴트입니다. "
            + "제공된 tools를 사용하여 사용자를 도와줘. "
            + "tool을 호출하면 결과를 기반으로 반드시 응답해.",
        }
    ]

    for i in range(2):                                  # 사용자 대화 두 번 처리
        chat_log.append(
            {
                "role": "user",
                "content": input("User > "),            # 사용자 입력 받기
            }
        )
        response = get_response(chat_log, tools=tools)
        print("AI > ", response.content)
        chat_log.append(response)


if __name__ == "__main__":
    main()
    

"""

- 셀 출력
    User > 2025년 8월에 주문한 고객은 누구야?
    데이터 조회중...완료
    AI >  2025년 8월에 주문한 고객은 홍길동입니다.
    User > 홍길동이 주문한 상품은 뭐야?
    데이터 조회중...완료
    AI >  홍길동이 주문한 주상품은 사과입니다.

"""

"""
- `test.db` 바탕으로 한 질문 입력 에시 
    test.db 바탕으로 한 질문 입력 예시_1 : 홍길동 고객의 최근 주문 내역을 보여줘. → 그 주문의 상태를 '배송중'으로 바꾸고 다시 보여줘.
    test.db 바탕으로 한 질문 입력 예시_2 : “김영희의 모든 주문 내역을 보여줘”
    test.db 바탕으로 한 질문 입력 예시_3 : “2025년 8월에 주문한 고객은 누구야?”
    test.db 바탕으로 한 질문 입력 예시_4 : “가장 많이 주문된 상품은 뭐야?”
    test.db 바탕으로 한 질문 입력 예시_5 : “2025년 8월에 주문한 고객은 누구야?”
    test.db 바탕으로 한 질문 입력 예시_6 : “사과를 주문한 고객 목록 알려줘”
    test.db 바탕으로 한 질문 입력 예시_7 : “홍길동의 주문 상태를 최신으로 업데이트해줘”
"""