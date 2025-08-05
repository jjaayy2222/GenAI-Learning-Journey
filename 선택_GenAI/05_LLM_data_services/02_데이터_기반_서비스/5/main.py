import json
import json.tool
import time
import os

# OpenAI 관련
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage         # 응답 메시지 타입

from utils import function_to_json_schema
from web import search_web

# 서드파티 라이브러리
import pandas as pd                 
from dotenv import load_dotenv     

# OpenAI 클라이언트 초기화
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 사용 가능한 함수 목록
functions = [search_web]
tools = []

# 자동으로 함수를 JSON 스키마로 변환하고 도구에 추가
for func in functions:
    schema = function_to_json_schema(func)
    tools.append(schema)


def call_function(func_name: str, args: dict) -> str:
    "이름이 func_name인 함수를 args로 호출하고 결과를 문자열로 반환합니다."

    print(func_name, args, "...", end="")

    for func in functions:
        if func.__name__ == func_name:
            result = func(**args)
            print("done.", end="\n")
            return str(result)
    print("not found.", end="\n")
    return f"Function '{func_name}' not found."


def get_response(
    chat_log: list, tools: dict = None, retry_count: int = 0
) -> ChatCompletionMessage:
    "OpenAI API를 사용하여 챗봇의 응답을 가져옵니다."

    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=chat_log, tools=tools
    )
    chat_log.append(response.choices[0].message)
    last_message = response.choices[0].message

    if last_message.tool_calls:
        if retry_count >= 3:
            return response.choices[0].message

        for tool_call in last_message.tool_calls:
            call_id = tool_call.id

            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            try:
                result = call_function(func_name, args)
                chat_log.append(
                    {
                        "tool_call_id": call_id,
                        "role": "tool",
                        "content": json.dumps(
                            {"result": result}, ensure_ascii=False
                        ),
                    }
                )
            except:
                chat_log.append(
                    {
                        "tool_call_id": call_id,
                        "role": "tool",
                        "content": "Error calling function.",
                    }
                )

        resp_message = get_response(
            chat_log, tools=tools, retry_count=retry_count + 1
        )
        return resp_message
    else:
        return response.choices[0].message


def main():
    chat_log = [
        {
            "role": "system",
            "content": f"""너는 사용자에 물음에 답하는 인공지능 챗봇이야.\ncurrent_time: {time.strftime("%Y-%m-%d %H:%M:%S")}(%Y-%m-%d %H:%M:%S)""",
        }
    ]

    for i in range(2):
        chat_log.append({"role": "user", "content": "user:" + input("User> ")})
        response = get_response(chat_log, tools=tools)
        print("AI>", response.content)


if __name__ == "__main__":
    main()


# test 
"""test_1

    User> 일론 머스크 뉴스
    search_web {'query': '일론 머스크 뉴스'} ...done.
    AI> 최근 일론 머스크에 관한 주요 뉴스는 다음과 같습니다:

    1. **테슬라, 40조 원 보상안 승인**: 테슬라의 이사회는 일론 머스크 CEO에게 약 290억 달러(약 40조 원) 규모의 신규 주식 보상안을 부여하기로 결정했습니다. 이 보상안은 머스크가 경영진으로서 2년간 지속적으로 역할을 수행해야 하는 조건이 붙어 있습니다. 이번 결정은 과거 선례인 850억 달러 규모의 보상안과는 구별되며, 주주들 간에는 '머스크 프리미엄'과 '머스크 리스크'에 대한 우려가 커지고 있습니다.

    2. **새로운 주식 지급**: 테슬라는 머스크에게 9600만 주의 주식을 승인했으며, 이는 그의 주식 소유 비율을 기존 13%에서 16%로 증가시키는 효과가 있습니다. 이 보상안은 테슬라의 실적 악화 속에서도 머스크가 집중할 수 있도록 하기 위한 조치로 해석되고 있습니다.

    3. **기관투자자와의 관계**: 머스크는 25%의 지분을 확보하여 기관투자자로부터 견제받지 않는 수준에 도달하는 것을 목표로 하고 있으며, 이는 그의 인공지능 및 자율주행 기술 개발에 집중할 수 있는 기반이 될 수 있습니다.

    4. **업계의 반응**: 테슬라가 중국과 미국을 포함한 여러 주요 시장에서 전기차 판매에 어려움을 겪고 있는 상황에서, 이러한 결정은 기업의 경영 투명성과 주주 가치를 중시하는 기관 투자자들의 우려를 불러일으킬 수 있습니다.

    현재 머스크와 테슬라의 미래 동향에 대해 많은 관심이 집중되고 있으며, 그의 결정과 테슬라의 성과가 앞으로 어떻게 전개될지 주목되고 있습니다.

    User> Grok 관련 최신 뉴스
    search_web {'query': 'Grok 뉴스'} ...done.
    AI> 최근 Grok에 대한 주요 뉴스는 다음과 같습니다:

    1. **Grok에 동영상 생성 기능 추가**: X 플랫폼에 탑재된 AI 어시스턴트 'Grok'에 'Imagine'이라는 새로운 동영상 생성 기능이 추가되었습니다. 이 기능은 6초짜리 음성 동영상을 생성할 수 있으며, Elon Musk는 이를 과거의 쇼트 동영상 공유 앱 'Vine'의 이름을 따서 'Grok Imagine'으로 부르고 있습니다. Grok Imagine은 사용자가 손쉽게 짧은 동영상을 만들 수 있도록 도와주는 기능입니다.

    2. **Grok 관련 인권 우려**: 일론 머스크의 xAI는 직원들에게 Grok의 학습용으로 자신의 얼굴 표정을 제공하도록 요청했습니다. 많은 직원이 개인정보 유출 우려로 이를 거부하고 있는 상황으로, AI 개발 단계에서 발생할 수 있는 인권 침해 문제로 비판받고 있습니다.

    3. **Grok 4의 출시**: Grok 4는 xAI의 최신 모델로, 뛰어난 성능과 병렬 처리가 가능하도록 설계되었습니다. 최신 AI 성능을 가진 Grok 4는 다양한 새로운 기능들을 갖추고 있으며, SuperGrok 및 Premium+ 구독자에게 제공되고 있습니다.

    4. **Grok과 AI 기술의 발전**: Grok 4의 성공은 대량의 GPU와 데이터 처리 능력에 기반하고 있으며, 이는 AI 성능의 비밀이 자본과 기술 인프라에 달려있음을 보여줍니다. Grok 4는 AI 개발에서의 혁신적인 접근보다는 하드웨어와 자원의 규모를 통한 성과를 보여주고 있습니다.

    이러한 내용들은 Grok이 AI 기술에서 어떻게 발전하고 있으며, 그로 인해 발생하는 사회적 및 윤리적 논란에 대한 관심을 불러일으키고 있습니다.
"""


"""test_2

    User> 클로드 코딩 뉴스
    search_web {'query': '클로드 코딩 뉴스'} ...done.
    AI> 최근 클로드에 관한 주요 뉴스는 앤트로픽과 오픈AI 간의 API 접근 차단과 관련된 것입니다. 앤트로픽은 오픈AI가 자신의 AI 모델 클로드(Claude)를 API를 통해 무단으로 사용하여 약관을 위반했다고 주장하며 접근 차단을 통보했습니다.

    1. **앤트로픽의 결정**: 앤트로픽은 오픈AI가 클로드 API를 사용하여 자사 도구와 연동하고 GPT-5의 개발을 평가한 점을 문제 삼았습니다. 이로 인해 앤트로픽은 오픈AI에 클로드 API 사용을 중단하겠다고 밝힌 것입니다. 관련 기사에 따르면, 클로드는 이미 많은 개발자들 사이에서 인기 있는 도구로 자리 잡고 있으며, 이와 관련된 사용이 금지되는 이유는 경쟁 제품 개발 및 AI 모델 훈련과 같은 행위가 포함되어 있기 때문입니다.

    2. **오픈AI의 반응**: 오픈AI는 앤트로픽의 행위가 일반적인 업계 관행이라며 유감의 뜻을 표했습니다. 오픈AI는 클로드를 사용해 자사 모델의 안전성과 성능을 개선해왔으며, 여전히 앤트로픽에 API 접근이 열려 있다고 주장했습니다.

    3. **GPT-5의 성능 향상**: 또한, 출시가 임박한 GPT-5에 대한 초기 사용자들의 반응이 긍정적이라는 소식도 전해졌습니다. 일부 사용자들은 GPT-5가 클로드 4보다 뛰어난 코딩 능력을 보여주었다고 언급했습니다. GPT-5는 다양한 분야에서의 성능 향상이 이루어졌다고 알려져 있으며, 이는 소프트웨어 엔지니어링에 특히 두드러졌습니다.

    이와 같은 내용은 AI 산업 내 경쟁과 혁신을 보여주는 중요한 여파를 드러내고 있습니다.
    
    User> 바이브 코딩
    search_web {'query': '바이브 코딩'} ...done.
    AI> "바이브 코딩"은 인공지능의 도움을 받아 코드를 작성하는 방식으로, 개발자가 사전 준비 없이 직감과 느낌에 의해 코딩할 수 있도록 해주는 신조어입니다. 이 개념은 2025년 안드레 카파시가 처음 언급한 이후 주목받고 있습니다.

    ### 바이브 코딩의 특징:

    1. **직관적 코드 작성**: 사용자들은 복잡한 논리나 준비 없이도 간단한 영어 프롬프트로 원하는 코드를 생성할 수 있습니다. 이는 프로그래밍에 대한 깊은 이해 없이도 코드 작성이 가능하다는 장점을 제공합니다.

    2. **생산성 향상**: 바이브 코딩은 프로토타입이나 간단한 기능 구현 단계에서 특히 유용하게 사용될 수 있습니다. 사용자들은 인공지능의 생성 코드를 빠르게 피드백하고, 실수를 줄이면서 개발 시간을 단축할 수 있습니다.

    3. **인공지능의 발전**: 바이브 코딩의 적용은 자연어 기반으로 작동하는 생성형 AI의 발전과 관련이 있으며, 개발 방식의 경계를 흐리게 하고 있습니다.

    4. **주요 툴과 응용**: GitHub Copilot 같은 도구가 바이브 코딩 방식으로 잘 알려져 있으며, 이를 통해 사용자들은 손쉽게 코드를 생성하고 프로젝트를 개발할 수 있습니다.

    5. **기술적 한계**: 모든 프로젝트에서 바이브 코딩이 효과적인 것은 아닙니다. 복잡한 프로젝트에서는 여전히 체계적인 설계와 관리를 해야 하며, 초기 프로토타입 이후 기술 부채가 증가할 수 있는 위험이 있습니다.

    최근의 논의에서도 바이브 코딩이 AI와 결합된 새로운 연구 패러다임으로 확장되고 있는 모습을 보여주고 있습니다. 구현 방식과 피드백 메커니즘을 잘 결합하면, 비전문가들도 프로그래밍 작업을 쉽게 수행할 수 있는 새로운 기회를 열어줄 수 있습니다.
"""


"""test_3
    User> 2025년 8월 6일 서울 날씨
    search_web {'query': '2025년 8월 6일 서울 날씨'} ...done.
    AI> 2025년 8월 6일 서울의 날씨는 비가 오는 것으로 예상됩니다. 현재 기온은 약 25도이며, 최대 기온은 27도, 최저 기온은 25도입니다. 습도는 88%로 높고, 바람은 시속 1.6m로 불고 있습니다.

    특히, 이 날은 우산이 필요할 확률이 높고, 야외 활동은 불편할 수 있다고 합니다. 날씨 정보는 계속해서 변동될 수 있으니, 외출 전 최신 정보 확인이 필요할 것입니다.
    
    User> 2025년 8월 6일 한국에 다른 지역에도 비가 와?
    search_web {'query': '2025년 8월 6일 한국 다른 지역 비 날씨'} ...done.
    AI> 2025년 8월 6일에는 한국 전역에서 비가 오는 것으로 예상됩니다. 중부 및 강원 지역에는 특히 많은 비가 내릴 것으로 보이며, 예보에 따르면 최대 120mm 이상의 폭우가 예상됩니다. 수도권 역시 출근길에 약 70mm의 비가 내릴 수 있으니, 우산을 챙기는 것이 좋습니다. 

    따라서 한국의 다른 지역에서도 비가 올 것으로 보이며, 전반적으로 강한 비와 함께 기상 변화가 있을 것으로 예상됩니다.
"""
