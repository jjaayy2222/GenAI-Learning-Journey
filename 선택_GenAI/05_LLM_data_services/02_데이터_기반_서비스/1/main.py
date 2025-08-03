# 표준 라이브러리
import os                          # 환경 변수 접근용
import sys                         # 시스템 설정 (입출력 등)
import json                        # JSON 파싱/생성
from pprint import pprint          # 디버깅용 출력 포맷

# 표준 입력 인코딩 설정 (한글 입력 문제 방지)
sys.stdin.reconfigure(encoding="utf-8")

# 서드파티 라이브러리
import pandas as pd                # CSV 파일 및 데이터프레임 처리
from dotenv import load_dotenv     # .env 파일에서 환경 변수 로드

# OpenAI 관련
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage  # 응답 메시지 타입

# OpenAI 클라이언트 초기화
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# 제품 목록에서 키워드를 포함한 제품을 검색
def find_products(keywords: list[str]) -> list[dict]:
    """제품 설명에 keywords가 포함된 제품을 찾아 반환합니다."""
    print("find_products 함수 실행:", keywords)

    # 현재 스크립트 경로 기준으로 파일 읽기
    csv_path = os.path.join(os.path.dirname(__file__), "product_list.csv")
    df = pd.read_csv(csv_path)

    # description 컬럼에서 키워드 포함 여부 검색 (대소문자 무시)
    result = df[df["description"].fillna("").str.contains("|".join(keywords), case=False)]
    return result.to_dict(orient="records")


# Chat log 기반 응답 생성 (함수 호출이 포함되면 실행까지)
def get_response(chat_log: list, tools: list = None) -> ChatCompletionMessage:
    # 우선 1차 응답을 받음
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=chat_log,
        tools=tools
    )

    # 함수 호출이 감지되면 실제 실행
    if response.choices[0].message.tool_calls:
        tool_call_results = []

        for tool_call in response.choices[0].message.tool_calls:
            call_id = tool_call.id

            # 호출된 함수가 find_products일 경우 실행
            if tool_call.function.name == "find_products":
                # 키워드 파싱
                keywords = json.loads(tool_call.function.arguments)["keywords"]
                products = find_products(keywords)

                # 함수 실행 결과 메시지 구성
                call_result_message = {
                    "tool_call_id": call_id,
                    "role": "tool",
                    "content": json.dumps(
                        {"keywords": keywords, "products": str(products)},
                        ensure_ascii=False,
                    ),
                }
                tool_call_results.append(call_result_message)

        # 원래 메시지 + 함수 실행 결과 메시지를 합쳐 다시 요청
        messages = chat_log + [response.choices[0].message] + tool_call_results
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
        )

    # 최종 응답 반환
    return response.choices[0].message


# find_products 함수를 tool로 정의 (GPT가 호출 가능하게 등록)
find_products_info = {
    "name": "find_products",
    "description": (
        "제품 설명에 keywords가 포함된 제품을 찾아서 반환합니다. "
        "찾고자 하는 keywords는 사용자가 요청한 내용과 관련된 제품을 필터링할 수 있는 적절한 키워드여야 합니다."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "keywords": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "상품 목록에서 검색할 키워드들. "
                    "이 키워드는 한글 문자열로 구성되어 있고, "
                    "하나라도 포함된 상품을 모두 가져오기에 적절한 키워드만 전달해야 합니다."
                ),
            },
        },
        "required": ["keywords"],
        "additionalProperties": False,
    },
}

tools = [{"type": "function", "function": find_products_info}]


# 📌 실행 진입점: 사용자 입력을 받아 응답 생성
def main():
    # 시스템 메시지: AI 역할 정의
    chat_log = [
        {
            "role": "system",
            "content": (
                "너는 쇼핑 마트의 AI 챗봇이야. "
                "다양한 제품에 대해 물어보거나 추천을 하는 용도야. "
                "추천을 할 때는 상품 목록에서 사용자가 원하는 상품만 선별해서 추천해야 해."
            ),
        },
    ]

    # 사용자 메시지 입력
    chat_log.append({
        "role": "user",
        "content": input("You> ")
    })

    # GPT 응답 가져오기
    response = get_response(chat_log, tools=tools)
    print("AI>", response.content)


# 메인 실행
if __name__ == "__main__":
    main()


    """
    - 셀 출력
    
        You> 다이어트 식품 추천해줘
        find_products 함수 실행: ['식품']
        AI> 여기 다양한 식품 추천 목록입니다:

        1. **다이어트 샐러드A**
        - **가격:** 7,000원
        - **설명:** 완제품 샐러드, 다이어트 식품
        - **알레르기 주의:** 아몬드가 포함되어 견과류 알러지 주의
        - **재고:** 10개

        2. **다이어트 샐러드B**
        - **가격:** 9,000원
        - **설명:** 완제품 샐러드, 다이어트 식품, 다이어트 샐러드A에서 아몬드 대신 연어를 추가
        - **재고:** 5개

        3. **초코 프로틴바**
        - **가격:** 3,500원
        - **설명:** 고단백 초콜릿 바, 50g, 다이어트 식품
        - **알레르기 주의:** 견과류 알러지 주의
        - **재고:** 15개

        4. **바나나 프로틴쉐이크**
        - **가격:** 5,500원
        - **설명:** 바나나 맛 단백질 쉐이크, 350ml, 다이어트 식품
        - **알레르기 주의:** 유당 불내증 주의
        - **재고:** 10개

        5. **닭가슴살 스낵**
        - **가격:** 4,000원
        - **설명:** 고단백 저지방 닭가슴살 스낵, 50g, 다이어트 식품
        - **재고:** 20개

        6. **매콤한 비건 버거**
        - **가격:** 7,800원
        - **설명:** 채식주의자를 위한 매콤한 비건 버거, 다이어트 식품
        - **알레르기 주의:** 견과류 알러지 주의
        - **재고:** 8개

        7. **아보카도 샐러드**
        - **가격:** 8,500원
        - **설명:** 아보카도와 다양한 채소가 포함된 샐러드, 다이어트 식품
        - **알레르기 주의:** 견과류 알러지 주의
        - **재고:** 7개

        8. **퀴노아 샐러드**
        - **가격:** 9,000원
        - **설명:** 퀴노아와 야채가 가득한 샐러드, 다이어트 식품
        - **재고:** 5개

        이 외에도 더 많은 식품이 있으니 관심 있는 제품이 있으면 말씀해 주세요!
    
    """