# Python과 SQL 연동 실습: 환경변수 기반 데이터베이스 연결

**작성일**: 2025-08-03  
**디렉터리**: `/2/`  
**학습 목표**: Python을 통한 MySQL 데이터베이스 연결 및 쿼리 실행

## 📋 프로젝트 구성 개요

```
/2/
├── .env                # 환경변수 설정 파일 (DB 접속 정보)
├── db.py               # 데이터베이스 연결 모듈
├── main.py             # 메인 실행 파일
├── schema.sql          # 테이블 구조 정의
├── scripts.sql         # 더미 데이터 삽입
└── test.db             # MySQL 데이터베이스 파일
```

---

## 🔐 1. 환경변수 설정 (.env)

### **개념 및 보안 중요성**
- **민감한 정보 분리**: DB 접속 정보를 코드에서 분리
- **환경별 관리**: 개발/테스트/프로덕션 환경별 다른 설정
- **보안 강화**: `.env` 파일을 `.gitignore`에 추가하여 버전 관리에서 제외

### **.env 파일 구성**
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=test_db
```

### **보안 체크리스트**
- ✅ `.env` 파일을 `.gitignore`에 추가
- ✅ 실제 비밀번호는 절대 코드에 하드코딩하지 않기
- ✅ 환경변수에 기본값 설정으로 오류 방지

---

## 🔧 2. db.py - 데이터베이스 연결 모듈

### **개념 및 역할**
- **MySQL 데이터베이스에 연결하고 쿼리를 실행하는 모듈**
- `.env` 파일에서 DB 접속 정보를 불러와 보안성을 높임
- 커넥션 객체를 반환하거나, 쿼리 실행 후 결과를 리스트로 반환

### **주요 기능 요약**
- `load_dotenv()`: 루트 경로에 있는 `.env` 파일에서 환경변수 로딩
- `get_connection()`: pymysql로 DB 연결을 생성
- `query_db(query: str)`: 주어진 SQL 쿼리를 실행하고, 결과를 dict 형태의 리스트로 반환

### **전체 코드**
```python
# db.py

import os
from dotenv import load_dotenv
import pymysql

# .env 파일에서 환경변수 로드
load_dotenv()

# 환경변수에서 DB 설정 가져오기 (기본값 포함)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'test_db')

def get_connection():
    """MySQL 데이터베이스 연결 생성"""
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor                          # 결과를 dict 형태로 반환
    )

def query_db(query: str) -> list:
    """SQL 쿼리 실행 및 결과 반환"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()                                    # 모든 결과를 리스트로 반환
    finally:
        conn.close()                                                    # 연결 해제
```

### **핵심 특징**
- **DictCursor**: 결과를 딕셔너리 형태로 반환하여 컬럼명으로 접근 가능
- **자동 연결 해제**: `try-finally` 구문으로 안전한 리소스 관리
- **기본값 설정**: `os.getenv()`의 두 번째 인자로 기본값 제공

---

## 🖥️ 3. main.py - 메인 실행 파일

### **개념 및 역할**
- **db.py에서 정의한 `query_db()`를 import하여 사용**
- 특정 order_id에 해당하는 주문 정보를 SQL로 조회
- 결과를 예쁘게 출력하기 위해 `tabulate` 사용

### **주요 기능 요약**
- MySQL에서 주문 정보, 고객 정보, 상품 정보, 상태 정보를 JOIN해서 조회
- `tabulate`를 통해 표 형태로 결과 출력

### **전체 코드**
```python
# main.py

from db import query_db
from tabulate import tabulate                                          # pip install tabulate 필요

# 복합 JOIN 쿼리: 주문 상세 정보 조회
query = """
SELECT  
    o.order_id, 
    o.customer_id, 
    o.order_date, 
    s.status_name, 
    GROUP_CONCAT(p.product_name ORDER BY p.product_id SEPARATOR ', ') AS products, 
    SUM(oi.quantity) AS total_quantity 
FROM  
    TB_ORDERS o 
JOIN  
    TB_ORDER_ITEMS oi ON o.order_id = oi.order_id 
JOIN  
    TB_PRODUCTS p ON oi.product_id = p.product_id 
JOIN  
    TB_ORDER_STATUS s ON o.status_id = s.status_id 
WHERE  
    o.order_id = 1003 
GROUP BY  
    o.order_id, o.customer_id, o.order_date, s.status_name;
"""

# 쿼리 실행
result = query_db(query)

# 결과 출력
if result:
    print("📊 주문 상세 정보")
    print("=" * 50)
    print(tabulate(result, headers="keys", tablefmt="grid"))
else:
    print("❌ No results found.")
```

### **SQL 쿼리 분석**
- **4개 테이블 JOIN**: 주문, 주문상품, 상품, 주문상태
- **GROUP_CONCAT**: 여러 상품을 하나의 문자열로 연결
- **GROUP BY**: 주문별로 데이터 그룹화
- **SUM**: 주문별 총 수량 계산

---

## 🚀 4. 실행 과정 및 결과

### **실행 순서**
```bash
# 1. 필요한 패키지 설치
pip install pymysql python-dotenv tabulate

# 2. .env 파일 생성 및 DB 정보 입력
touch .env

# 3. 메인 파일 실행
python main.py
```

### **실행 결과 예시**
```
📊 주문 상세 정보
==================================================
+------------+---------------+--------------+---------------+------------+------------------+
|   order_id |   customer_id | order_date   | status_name   | products   |   total_quantity |
+============+===============+==============+===============+============+==================+
|       1003 |             7 | 2025-08-03   | 주문접수          | 사과         |                1 |
+------------+---------------+--------------+---------------+------------+------------------+
```

  * ![실제 출력 화면](/선택_GenAI/05_LLM_data_services/02_데이터_기반_서비스/3/mainpy_result.png)


### **결과 데이터 해석**
- **order_id 1003**: 조회한 주문 번호
- **customer_id 7**: 홍길동 고객
- **order_date**: 2025-08-03 주문일
- **status_name**: 주문접수 상태
- **products**: 사과 1개 주문
- **total_quantity**: 총 수량 1개

---

## 📊 5. 아키텍처 및 모듈 분리

### **모듈별 책임**

| 모듈 | 역할 | 핵심 기능 |
|------|------|-----------|
| **db.py** | 🔧 백엔드 모듈 | DB 연결 및 쿼리 실행만 담당 |
| **main.py** | 🖥️ 프론트엔드 모듈 | 실질적인 쿼리 실행과 사용자 출력 처리 |
| **.env** | 🔐 설정 모듈 | 민감 정보 관리 |

### **장점**
- **관심사 분리**: DB 로직과 비즈니스 로직 분리
- **재사용성**: `db.py`는 다른 프로젝트에서도 재사용 가능
- **유지보수성**: DB 설정 변경 시 `.env`만 수정하면 됨

## 🛠️ 6. 추가 활용 예시

### **다중 쿼리 실행**
```python
# main.py 확장 예시

# 고객별 주문 통계
customer_stats = query_db("""
    SELECT c.customer_name, COUNT(o.order_id) as order_count
    FROM TB_CUSTOMERS c
    LEFT JOIN TB_ORDERS o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
""")

# 인기 상품 Top 3
popular_products = query_db("""
    SELECT p.product_name, SUM(oi.quantity) as total_sold
    FROM TB_PRODUCTS p
    JOIN TB_ORDER_ITEMS oi ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.product_name
    ORDER BY total_sold DESC
    LIMIT 3
""")

print("👥 고객별 주문 통계")
print(tabulate(customer_stats, headers="keys", tablefmt="grid"))

print("\n🏆 인기 상품 Top 3")
print(tabulate(popular_products, headers="keys", tablefmt="grid"))
```

### **데이터 삽입 기능 추가**
```python
# db.py에 추가할 함수
def execute_db(query: str, params=None):
    """INSERT, UPDATE, DELETE 쿼리 실행"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount  # 영향받은 행 수 반환
    finally:
        conn.close()

# 사용 예시
new_customer = execute_db(
    "INSERT INTO TB_CUSTOMERS (customer_name) VALUES (%s)", 
    ("박민수",)
)
print(f"✅ {new_customer}개의 고객 정보가 추가되었습니다.")
```

---

## 🔍 7. 문제 해결 및 디버깅

### **자주 발생하는 오류들**

#### **ModuleNotFoundError**
```bash
# 해결방법: 필요한 패키지 설치
pip install pymysql python-dotenv tabulate
```

#### **Connection Error**
```python
# .env 파일 확인 포인트
DB_HOST=localhost        # ✅ 올바른 호스트
DB_PORT=3306             # ✅ 올바른 포트
DB_PASSWORD=             # ⚠️ 실제 비밀번호 입력 필요
```

#### **Empty Result**
```python
# 디버깅용 쿼리 추가
def debug_query(query: str):
    print(f"🔍 실행 쿼리: {query}")
    result = query_db(query)
    print(f"📊 결과 개수: {len(result)}")
    return result
```

## ✅ 8. 학습 성과 및 다음 단계

### **완성된 기술 스택**
- ✅ **환경변수 관리**: `.env`를 통한 보안 설정
- ✅ **데이터베이스 연결**: `pymysql` 활용
- ✅ **쿼리 실행**: `SELECT`, `JOIN`, `GROUP BY` 활용
- ✅ **결과 출력**: `tabulate`를 통한 가독성 향상
- ✅ **모듈 분리**: 재사용 가능한 `db.py` 모듈 작성

### **실무 활용도**
- 🎯 **웹 개발**: Flask/Django에서 데이터베이스 연동
- 🎯 **데이터 분석**: pandas와 연동하여 대용량 데이터 처리
- 🎯 **자동화**: 정기적인 데이터 리포트 생성

### **다음 학습 방향**
- [ ] **ORM 학습**: SQLAlchemy, Django ORM
- [ ] **연결 풀링**: 성능 최적화를 위한 커넥션 풀 활용
- [ ] **비동기 처리**: asyncio와 aiomysql 활용
- [ ] **데이터 시각화**: matplotlib, plotly와 연동

---

## 💡 핵심 요약

### **🔑 주요 배운 점**
1. **모듈화의 중요성**: DB 로직과 비즈니스 로직의 분리
2. **보안 의식**: **환경변수**를 통한 민감 정보 관리
3. **자원 관리**: try-finally를 통한 안전한 DB 연결 해제
4. **사용자 경험**: `tabulate`를 통한 직관적인 결과 출력
