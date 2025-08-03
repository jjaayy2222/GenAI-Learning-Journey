# SQL과 ChatGPT 연동 시스템: 자연어 기반 데이터베이스 질의응답

**작성일**: 2025-08-03  
**디렉터리**: `/4/`  
**학습 목표**: OpenAI GPT와 MySQL을 연동한 자연어 기반 DB 질의응답 시스템 구축

---

## 🎯 시스템 아키텍처 개요

```
사용자 자연어 질문
    ↓
main.py (GPT API 호출)
    ↓
GPT가 SQL 쿼리 생성 및 tool_call
    ↓
db.py (query_db 함수 실행)
    ↓
session.py (DB 연결 관리)
    ↓
MySQL 데이터베이스
    ↓
결과 반환 → GPT 재처리 → 자연어 응답
```

---

## 📁 프로젝트 파일 구성

```
/4/
├── .env          # 환경변수 (DB 정보 + OpenAI API 키)
├── session.py    # DB 연결 관리 모듈
├── db.py         # DB 쿼리 실행 모듈  
└── main.py       # GPT API 연동 및 대화 관리
```

## 🔐 1. session.py - DB 연결 관리

### **역할 및 목적**
- **MySQL 데이터베이스와의 연결을 담당하는 모듈**
- 환경변수(.env)를 불러와서 DB 접속 정보를 설정
- pymysql로 DB 커넥션 생성 후, conn 객체를 외부에 제공

### **핵심 코드**
```python
# session.py

import os
from dotenv import load_dotenv
import pymysql

# .env에서 환경변수 로드
load_dotenv()

# DB 연결 생성 (전역 변수로 관리)
conn = pymysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', 3306)),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    db=os.getenv('DB_NAME', 'test_db'),
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor  # 결과를 dict 형태로 반환
)
```

### **작동 순서**
1. `.env` 파일에서 DB 접속 정보 읽음
2. `pymysql.connect()`로 연결 생성
3. 생성된 `conn`을 `db.py` 등 다른 파일에서 `import` 해서 사용

### **결과 및 의미**
- ✅ **재사용 가능한 DB 커넥션**: 한 번 생성하여 모든 모듈에서 공유
- ✅ **환경변수 기반 보안**: 민감한 비밀번호 정보 분리 관리
- ✅ **DictCursor 활용**: 쿼리 결과를 딕셔너리 형태로 받아 GPT가 이해하기 쉽게 처리

---

## 📊 2. db.py - DB 쿼리 실행 모듈

### **역할 및 목적**
- **DB에 SQL 쿼리를 실행하는 함수 제공**
- `session.py`의 `conn`을 사용하여 쿼리 실행 및 결과 반환
- GPT가 요청한 SQL을 실제로 실행하는 핵심 모듈

### **핵심 코드**
```python
# db.py

from session import conn

def query_db(query: str) -> list:
    """쿼리를 실행하고 결과 리스트(dict) 반환"""
    
    print("데이터 조회중...", end="")
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            # 컬럼 이름과 데이터를 매핑하여 딕셔너리 리스트 생성
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(f"오류 발생: {e}")
        result = []
    
    print("완료")
    return result
```

### **작동 순서**
1. `conn.cursor()`로 커서 생성
2. 입력받은 SQL 쿼리 실행 (`cursor.execute()`)
3. 결과 행을 딕셔너리 리스트 형태로 변환하여 반환
4. 에러 발생 시 빈 리스트 반환 (시스템 안정성 보장)

### **결과 및 의미**
- ✅ **구조화된 결과**: SQL 쿼리 결과를 Python에서 쉽게 다룰 수 있도록 가공
- ✅ **추상화 레이어**: DB와의 연결 및 쿼리 실행을 추상화하여 재사용 용이
- ✅ **안전한 예외 처리**: 에러 발생 시 프로그램이 멈추지 않도록 보호

---

## 🤖 3. main.py - GPT API 연동 및 대화 관리

### **역할 및 목적**
- **사용자와의 대화 흐름 처리 및 OpenAI API 호출 담당**
- 사용자가 입력한 자연어를 받아 GPT 모델에 전달
- GPT가 SQL 쿼리 실행 요청 시 `db.py`의 `query_db` 함수 호출해 결과 받아 GPT에게 전달
- 최종 GPT 응답을 사용자에게 출력

### **핵심 코드**

#### **OpenAI 클라이언트 및 환경 설정**
```python
# main.py

import os
import json
from dotenv import load_dotenv
from db import query_db
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# GPT가 사용할 함수 정의 (Tool Function)
query_db_info = {
    "name": "query_db",
    "description": "MySQL 데이터베이스에서 SQL 쿼리를 실행하고 결과를 반환합니다.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "실행할 SQL 쿼리문"
            }
        },
        "required": ["query"]
    }
}
```

#### **GPT 응답 처리 함수**
```python
def get_response(chat_log: list, tools: dict = None):
    """GPT API 호출 및 tool_call 처리"""
    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=chat_log, 
        tools=tools
    )

    # GPT가 tool_call을 요청한 경우
    if response.choices[0].message.tool_calls:
        tool_call_results = []
        
        for tool_call in response.choices[0].message.tool_calls:
            call_id = tool_call.id
            
            # query_db 함수 호출 요청인 경우
            if tool_call.function.name == "query_db":
                # GPT가 생성한 SQL 쿼리 추출
                query_str = json.loads(tool_call.function.arguments)["query"]
                print(f"🔍 실행할 쿼리: {query_str}")
                
                # 실제 DB 쿼리 실행
                result = query_db(query_str)
                
                # 결과를 GPT가 이해할 수 있는 형태로 포장
                tool_call_results.append({
                    "tool_call_id": call_id,
                    "role": "tool",
                    "content": json.dumps({"result": str(result)}, ensure_ascii=False),
                })
        
        # 쿼리 결과를 포함해서 GPT에게 재요청
        chat_log += [response.choices[0].message] + tool_call_results
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=chat_log, 
            tools=tools
        )
    
    return response.choices[0].message
```

#### **메인 대화 루프**
```python
def main():
    # GPT가 사용할 수 있는 도구 정의
    tools = [{"type": "function", "function": query_db_info}]
    
    # 시스템 메시지 설정
    chat_log = [{
        "role": "system",
        "content": "너는 유용한 고객 지원 어시스턴트입니다. 제공된 tools를 사용하여 사용자를 도와줘."
    }]

    print("🤖 ChatGPT 기반 데이터베이스 질의응답 시스템")
    print("=" * 50)
    
    for i in range(2):  # 2회 대화 시도
        user_input = input(f"\n[{i+1}/2] User> ")
        chat_log.append({"role": "user", "content": user_input})
        
        response = get_response(chat_log, tools=tools)
        print("AI>", response.content)
        
        chat_log.append(response)

if __name__ == "__main__":
    main()
```

### **작동 순서**
1. 환경변수에서 OpenAI API 키를 로드
2. `main()`에서 시스템 메시지 세팅 및 2번 대화 루프 실행
3. 사용자가 질문 입력 → GPT에게 전달
4. GPT가 DB 쿼리 필요 시 `query_db` tool_call 요청
5. `db.py`의 `query_db()` 함수 호출하여 실제 SQL 실행
6. 쿼리 결과를 GPT에 재전달
7. GPT가 결과를 분석하여 자연어로 최종 응답 생성

### **결과 및 의미**
- ✅ **자연어 → SQL 변환**: 사용자의 자연어 질문을 자동으로 SQL로 변환
- ✅ **Tool Call 활용**: GPT-4의 함수 호출 기능을 실제 업무에 적용
- ✅ **완전 자동화**: DB 쿼리부터 결과 해석까지 모든 과정 자동화

---

## 🚀 4. 실제 실행 예시

### **대화 예시 1: 고객 정보 조회**
```
[1/2] User> 홍길동 고객의 주문 내역을 보여줘

🔍 실행할 쿼리: SELECT o.order_id, o.order_date, p.product_name, oi.quantity 
FROM TB_ORDERS o 
JOIN TB_CUSTOMERS c ON o.customer_id = c.customer_id 
JOIN TB_ORDER_ITEMS oi ON o.order_id = oi.order_id 
JOIN TB_PRODUCTS p ON oi.product_id = p.product_id 
WHERE c.customer_name = '홍길동'

데이터 조회중...완료

AI> 홍길동 고객의 주문 내역을 확인했습니다. 2025-08-03에 주문번호 1003으로 사과 1개를 주문하셨네요. 현재 주문 상태는 '주문접수' 상태입니다.
```

### **대화 예시 2: 통계 정보 조회**
```
[2/2] User> 가장 많이 팔린 상품이 뭐야?

🔍 실행할 쿼리: SELECT p.product_name, SUM(oi.quantity) as total_sold 
FROM TB_PRODUCTS p 
JOIN TB_ORDER_ITEMS oi ON p.product_id = oi.product_id 
GROUP BY p.product_id, p.product_name 
ORDER BY total_sold DESC 
LIMIT 1

데이터 조회중...완료

AI> 현재까지 가장 많이 팔린 상품은 '사과'입니다. 총 1개가 판매되었습니다.
```

* ![실제 셀 출력](/선택_GenAI/05_LLM_data_services/02_데이터_기반_서비스/4/result3.png)

---

## 🔧 5. 환경변수 설정 (.env)

### **필수 환경변수**
```env
# MySQL 데이터베이스 설정
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=test_db

# OpenAI API 설정
OPENAI_API_KEY=your_openai_api_key_here
```

### **보안 체크리스트**
- ✅ `.env` 파일을 `.gitignore`에 추가
- ✅ `OpenAI API 키`는 **절대 코드에 하드코딩하지 않기**
- ✅ `DB 비밀번호`도 **환경변수**로 관리

---

## 📋 6. 시스템 요구사항 및 설치

### **필요 패키지**
```bash
pip install openai pymysql python-dotenv
```

### **실행 전 체크리스트**
- [ ] MySQL 서버 실행 중
- [ ] `test_db` 데이터베이스 및 테이블 존재
- [ ] `.env` 파일에 올바른 DB 정보 및 OpenAI API 키 설정
- [ ] 필요한 Python 패키지 설치 완료

### **실행 명령어**
```bash
cd /GenAI-Learning-Journey/선택_GenAI/05_LLM_data_services/02_데이터_기반_서비스/4/
python main.py
```

## ⚡ 7. 고급 기능 및 확장 가능성

### **현재 구현된 핵심 기능**
- ✅ **자연어 질의**: 사용자가 평상시 말하는 방식으로 DB 조회 가능
- ✅ **자동 SQL 생성**: GPT가 적절한 SQL 쿼리 자동 생성
- ✅ **결과 해석**: 쿼리 결과를 사용자가 이해하기 쉬운 자연어로 설명
- ✅ **에러 처리**: DB 오류 발생 시에도 시스템이 안정적으로 작동

### **확장 가능한 기능들**
```python
# 데이터 삽입 기능 추가 예시
insert_data_info = {
    "name": "insert_data",
    "description": "데이터베이스에 새로운 데이터를 삽입합니다.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "INSERT SQL 쿼리문"}
        },
        "required": ["query"]
    }
}

# 데이터 분석 기능 추가 예시  
analyze_data_info = {
    "name": "analyze_data",
    "description": "데이터 분석 및 시각화를 수행합니다.",
    "parameters": {
        "type": "object", 
        "properties": {
            "analysis_type": {"type": "string", "description": "분석 유형"}
        }
    }
}
```

## 📊 8. 파일별 역할 요약표

| 파일명 | 역할 | 주요 기능 | 결과 |
|--------|------|-----------|------|
| **session.py** | DB 접속 관리 | 환경변수 기반 DB 연결 생성 | 재사용 가능한 DB 커넥션 객체 |
| **db.py** | DB 쿼리 실행 함수 제공 | SQL 쿼리 실행 및 결과 반환 | 딕셔너리 리스트 형태 결과 |
| **main.py** | 대화 관리 및 GPT API 호출 | GPT 질문 처리 및 tool_call 연동 | 자연어 기반 DB 질의응답 시스템 |

## 🎯 9. 학습 성과 및 기술적 가치

### **완성된 기술 스택**
- ✅ **AI + Database 연동**: 최신 GPT-4와 전통적 DB의 결합
- ✅ **Tool Function 활용**: OpenAI의 최신 기능 적용
- ✅ **모듈화 설계**: 각 기능별로 명확하게 분리된 코드 구조
- ✅ **환경변수 보안 관리**: 실무에서 요구되는 보안 수준 구현

### **실무 적용 가능성**
- 🎯 **고객 지원 시스템**: 실시간 주문 조회, 배송 상태 확인
- 🎯 **비즈니스 인텔리전스**: 매출 분석, 고객 행동 분석
- 🎯 **내부 관리 도구**: 직원들이 자연어로 DB 조회 가능
- 🎯 **데이터 민주화**: SQL을 모르는 사용자도 데이터 활용 가능

  * 프름프트, 스크립트는 조금더 정교화 필요


### **기술적 혁신성**
**"데이터베이스 전문가가 아닌 일반 사용자도 복잡한 DB 쿼리를 자연어로 실행할 수 있게 만드는"** 접근법 구현.

## 💡 핵심 요약

### **🔑 핵심 학습 포인트**
1. **AI-DB 연동 패턴**: GPT의 tool_call 기능을 활용한 실시간 DB 연동
2. **모듈 분리의 중요성**: session, db, main 각각의 역할 분담
3. **사용자 경험 혁신**: 복잡한 SQL을 자연어로 대체
4. **확장 가능한 아키텍처**: 새로운 기능 추가가 용이한 구조
