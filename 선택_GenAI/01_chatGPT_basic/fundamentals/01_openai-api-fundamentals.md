# 01. OpenAI API 기초 개념과 시작하기

📁 위치: /GenAI-Learning-Journey/선택과정_생성형AI/01_ChatGPT_basic/01_openai-api-fundamentals.md  
📅 정리일: 2025-08-02  
📚 출처: OpenAI Official Documentation + 부트캠프 실습 연계

## 🎯 학습 목표

> OpenAI API의 기본 구조를 이해하고, 실제 개발 환경에서 API를 호출할 수 있는 기초 지식을 습득한다.  
> 부트캠프 실습에서 바로 활용할 수 있는 실전 가이드를 제공한다.

## 🧩 OpenAI API란 무엇인가?

OpenAI API는 GPT-4, GPT-3.5, DALL-E, Whisper 등 OpenAI의 AI 모델들을 HTTP 요청을 통해 사용할 수 있게 해주는 RESTful API입니다.

### 핵심 특징

```plaintext
- REST API 기반으로 모든 프로그래밍 언어에서 사용 가능
- JSON 형태의 요청/응답 구조
- 토큰 기반 과금 시스템
- 실시간 스트리밍 응답 지원
- 다양한 모델과 엔드포인트 제공
```

## 🔧 주요 API 엔드포인트

| 엔드포인트 | 용도 | 주요 모델 |
|------------|------|-----------|
| `/v1/chat/completions` | 채팅/대화형 완성 | GPT-4, GPT-3.5-turbo |
| `/v1/completions` | 텍스트 완성 | text-davinci-003 (레거시) |
| `/v1/images/generations` | 이미지 생성 | DALL-E 3, DALL-E 2 |
| `/v1/audio/transcriptions` | 음성-텍스트 변환 | Whisper |
| `/v1/embeddings` | 텍스트 임베딩 | text-embedding-ada-002 |

## 🏗 기본 API 호출 구조

### 1. HTTP 요청 형태

```plaintext
POST https://api.openai.com/v1/chat/completions
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "model": "gpt-4",
  "messages": [
    {"role": "user", "content": "Hello, world!"}
  ],
  "max_tokens": 100,
  "temperature": 0.7
}
```

### 2. Python 예제 (openai 라이브러리)

```plaintext
import openai
from openai import OpenAI

client = OpenAI(api_key='your-api-key-here')

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Hello, world!"}
    ],
    max_tokens=100,
    temperature=0.7
)

print(response.choices[0].message.content)
```

### 3. JavaScript 예제

```plaintext
const response = await fetch('https://api.openai.com/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  },
  body: JSON.stringify({
    model: 'gpt-4',
    messages: [
      {role: 'user', content: 'Hello, world!'}
    ],
    max_tokens: 100,
    temperature: 0.7
  })
});

const data = await response.json();
console.log(data.choices[0].message.content);
```

## 🎛 주요 모델 비교

### GPT-4 계열

| 모델명 | 최대 토큰 | 특징 | 권장 용도 |
|--------|-----------|------|-----------|
| gpt-4 | 8,192 | 높은 품질, 복잡한 추론 | 전문적 작업, 분석 |
| gpt-4-32k | 32,768 | 긴 컨텍스트 지원 | 장문 처리, 문서 분석 |
| gpt-4-turbo | 128,000 | 빠르고 비용효율적 | 일반적 대화, 개발 |

### GPT-3.5 계열

| 모델명 | 최대 토큰 | 특징 | 권장 용도 |
|--------|-----------|------|-----------|
| gpt-3.5-turbo | 16,385 | 빠르고 저렴 | 간단한 대화, 요약 |
| gpt-3.5-turbo-16k | 16,385 | 긴 컨텍스트 | 중간 길이 문서 처리 |

## ⚙️ 핵심 파라미터 설명

### 필수 파라미터

```plaintext
model: 사용할 AI 모델 지정
messages: 대화 내역 배열 (role + content 구조)
```

### 선택적 파라미터

```plaintext
max_tokens: 생성할 최대 토큰 수 (기본값: 모델별 상이)
temperature: 창의성 조절 (0.0~2.0, 기본값: 1.0)
  - 0에 가까울수록 일관된 답변
  - 2에 가까울수록 창의적 답변
top_p: 토큰 선택 다양성 (0.0~1.0, 기본값: 1.0)
stream: 실시간 스트리밍 여부 (true/false)
```

## 🔐 API 키 관리와 보안

### 1. API 키 발급

```plaintext
1. OpenAI Platform (https://platform.openai.com) 접속
2. 계정 생성/로그인
3. API Keys 메뉴에서 새 키 생성
4. 생성된 키를 안전한 곳에 저장 (재확인 불가)
```

### 2. 환경변수 설정

```plaintext
# .env 파일
OPENAI_API_KEY=sk-proj-your-key-here

# Python에서 사용
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
```

### 3. 보안 주의사항

```plaintext
- API 키를 코드에 직접 하드코딩하지 않기
- .env 파일을 .gitignore에 포함시키기
- 키가 노출되면 즉시 폐기하고 새로 생성
- 사용량 제한 및 알림 설정하기
```

## 💰 토큰과 비용 이해

### 토큰이란?

```plaintext
- AI가 텍스트를 처리하는 기본 단위
- 영어: 약 4자 = 1토큰
- 한국어: 약 1-2자 = 1토큰
- 입력(prompt) + 출력(completion) 모두 토큰으로 과금
```

### 비용 계산 예시 (2025년 8월 기준)

```plaintext
GPT-4:
- Input: $30/1M 토큰
- Output: $60/1M 토큰

GPT-3.5-turbo:
- Input: $1.50/1M 토큰  
- Output: $2.00/1M 토큰

예시: "안녕하세요"라는 질문(5토큰)에 100토큰 답변
→ GPT-4 사용시 약 $0.006 (약 8원)
```

## 🚀 첫 번째 실습: Hello World

### Python 환경 설정

```plaintext
# 가상환경 생성 및 활성화
python -m venv genai_env
source genai_env/bin/activate  # Windows: genai_env\Scripts\activate

# 필요한 패키지 설치
pip install openai python-dotenv
```

### 간단한 실습 코드

```plaintext
# hello_openai.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 클라이언트 초기화
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "안녕하세요! OpenAI API 첫 사용입니다."}
        ],
        max_tokens=50
    )
    
    print("AI 응답:", response.choices[0].message.content)
    print("사용 토큰:", response.usage.total_tokens)
    
except Exception as e:
    print("오류 발생:", str(e))
```

## 📋 체크리스트

- [ ] OpenAI Platform 계정 생성
- [ ] API 키 발급 및 환경변수 설정  
- [ ] Python/Node.js 개발환경 구성
- [ ] 첫 번째 API 호출 성공
- [ ] 토큰 사용량 및 비용 확인
- [ ] 에러 처리 및 예외상황 대응

## 🔗 관련 문서

- [02_prompt-engineering-principles.md](./02_prompt-engineering-principles.md) — 프롬프트 작성 원칙
- [03_message-roles-and-structure.md](./03_message-roles-and-structure.md) — 메시지 구조화
- [10_hands-on-api-practice.md](./10_hands-on-api-practice.md) — 실전 API 활용

## 📝 학습 노트

```plaintext
💡 오늘의 핵심 포인트:
1. OpenAI API는 HTTP 기반 RESTful 서비스
2. 토큰 기반 과금으로 비용 관리 필요
3. API 키 보안이 가장 중요
4. messages 배열 구조가 대화의 핵심

🤔 더 알아볼 점:
- 스트리밍 응답 활용법
- 함수 호출(Function Calling) 기능
- 파인튜닝을 통한 모델 커스터마이징
```

✅ 다음 문서 →  
📄 [02_prompt-engineering-principles.md](./02_prompt-engineering-principles.md): 효과적인 프롬프트 작성 원칙과 모범 사례
