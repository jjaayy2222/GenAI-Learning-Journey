# SQL & Database 기초 학습 정리

**작성일**: 2025-08-03  
**실습 환경**: MySQL 9.3.0, macOS  
**학습 목표**: SQL 기본 문법과 데이터베이스 관계형 구조 이해

## 📚 1. 핵심 개념

### 🗄️ **데이터베이스 기본 구조**

| 용어 | 설명 | 예시 |
|------|------|------|
| **데이터베이스(DB)** | 구조화된 데이터 저장소 | `test_db` |
| **테이블(Table)** | 행과 열로 이루어진 데이터 저장 단위 | `TB_CUSTOMERS` |
| **SQL** | 데이터베이스 조작 언어 | `SELECT * FROM TB_CUSTOMERS` |
| **DBMS** | 데이터베이스 관리 시스템 | MySQL, SQLite |

### 🔗 **관계형 데이터베이스의 핵심**
- **외래키(Foreign Key)**: 테이블 간 관계를 정의하는 제약조건
- **참조 무결성**: 부모-자식 관계에서 데이터 일관성 유지
- **제약조건**: 데이터 삽입/삭제 시 순서가 중요함

## 🛠️ 2. 실습 환경 구축 및 기본 조작

### **MySQL 접속**
```bash
mysql -u root -p
# 비밀번호 입력 후 접속
```

### **데이터베이스 현황 확인**
```sql
SHOW DATABASES;
```

**실행 결과:**
```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| test_db            |
+--------------------+
```

### **데이터베이스 선택 및 테이블 확인**
```sql
USE test_db;
SHOW TABLES;
```

**실행 결과:**
```
+-------------------+
| Tables_in_test_db |
+-------------------+
| TB_CUSTOMERS      |
| TB_ORDER_ITEMS    |
| TB_ORDER_STATUS   |
| TB_ORDERS         |
| TB_PRODUCTS       |
+-------------------+
```

## 📋 3. 테이블 구조 분석

### **고객 테이블 (TB_CUSTOMERS)**
```sql
DESC TB_CUSTOMERS;
```

**구조:**
```
+---------------+--------------+------+-----+---------+----------------+
| Field         | Type         | Null | Key | Default | Extra          |
+---------------+--------------+------+-----+---------+----------------+
| customer_id   | int          | NO   | PRI | NULL    | auto_increment |
| customer_name | varchar(100) | NO   |     | NULL    |                |
+---------------+--------------+------+-----+---------+----------------+
```

### **테이블 생성 예시**
```sql
CREATE TABLE TB_CUSTOMERS (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_name VARCHAR(100) NOT NULL
);
```

**핵심 포인트:**
- `AUTO_INCREMENT`: 자동으로 증가하는 기본키
- `PRIMARY KEY`: 테이블의 고유 식별자
- `NOT NULL`: 빈 값 허용 안 함

## 💾 4. 데이터 조작 실습

### **데이터 삽입 (INSERT)**
```sql
INSERT INTO TB_CUSTOMERS (customer_name) VALUES ('홍길동');
INSERT INTO TB_CUSTOMERS (customer_name) VALUES ('김영희');
INSERT INTO TB_CUSTOMERS (customer_name) VALUES ('이철수');
```

### **데이터 조회 (SELECT)**
```sql
SELECT * FROM TB_CUSTOMERS;
```

**실행 결과:**
```
+-------------+---------------+
| customer_id | customer_name |
+-------------+---------------+
|           7 | 홍길동        |
|           8 | 김영희        |
|           9 | 이철수        |
+-------------+---------------+
```

**💡 주의사항**: `customer_id`가 7부터 시작하는 이유는 이전에 데이터를 삭제했지만 `AUTO_INCREMENT` 값은 계속 증가하기 때문!

## ⚠️ 5. 외래키 제약조건과 데이터 삭제 순서

### **잘못된 삭제 시도**
```sql
TRUNCATE TABLE TB_CUSTOMERS;
-- ERROR 1701: Cannot truncate a table referenced in a foreign key constraint
```

```sql
DELETE FROM TB_ORDERS;
-- ERROR 1451: Cannot delete or update a parent row: a foreign key constraint fails
```

### **올바른 삭제 순서 (자식 → 부모)**
```sql
-- 1. 가장 하위 테이블부터 삭제
DELETE FROM TB_ORDER_ITEMS;  -- Query OK, 6 rows affected

-- 2. 중간 단계 테이블 삭제
DELETE FROM TB_ORDERS;       -- Query OK, 3 rows affected

-- 3. 부모 테이블 삭제
DELETE FROM TB_CUSTOMERS;    -- Query OK, 6 rows affected
```

**🔑 핵심 원칙**: 외래키로 참조되는 테이블은 참조하는 테이블의 데이터를 먼저 삭제해야 함!

## 🔗 6. 관계형 데이터 삽입 실습

### **기본 데이터 삽입**
```sql
-- 고객 정보
INSERT INTO TB_CUSTOMERS (customer_name) VALUES ('홍길동');

-- 제품 정보
INSERT INTO TB_PRODUCTS (product_name) VALUES ('노트북');

-- 주문 상태
INSERT INTO TB_ORDER_STATUS (status_name) VALUES ('주문완료');
```

### **관계형 데이터 삽입 시 주의사항**
```sql
-- ❌ 잘못된 예시: 존재하지 않는 customer_id 참조
INSERT INTO TB_ORDERS (customer_id, order_date, status_id) VALUES (1, '2025-08-03', 1);
-- ERROR 1452: Cannot add or update a child row: a foreign key constraint fails
```

```sql
-- ✅ 올바른 예시: 실제 존재하는 customer_id 사용
INSERT INTO TB_ORDERS (customer_id, order_date, status_id) VALUES (7, '2025-08-03', 1);
-- Query OK, 1 row affected
```

### **주문 상세 정보 확인**
```sql
SELECT order_id, customer_id, order_date, status_id 
FROM TB_ORDERS 
ORDER BY order_id DESC LIMIT 1;
```

**실행 결과:**
```
+----------+-------------+------------+-----------+
| order_id | customer_id | order_date | status_id |
+----------+-------------+------------+-----------+
|     1003 |           7 | 2025-08-03 |         1 |
+----------+-------------+------------+-----------+
```

## 🎯 7. 실습에서 배운 핵심 교훈

### **1. 외래키 제약조건의 중요성**
- ✅ **장점**: 데이터 무결성 보장, 잘못된 참조 방지
- ⚠️ **주의**: 삭제/삽입 순서를 반드시 고려해야 함

### **2. AUTO_INCREMENT의 특성**
- 데이터를 삭제해도 번호는 되돌아가지 않음
- 연속성보다는 **고유성**을 보장하는 것이 목적

### **3. 참조 무결성 유지**
```sql
-- 올바른 순서: 부모 데이터 먼저 확인
SELECT * FROM TB_CUSTOMERS;  -- customer_id 확인
SELECT * FROM TB_PRODUCTS;   -- product_id 확인

-- 그 다음 자식 데이터 삽입
INSERT INTO TB_ORDERS (customer_id, order_date, status_id) VALUES (7, '2025-08-03', 1);
```

## 🛡️ 8. 환경변수를 통한 보안 관리

### **.env 파일 설정**
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=test_db
```

### **Python 연동 예시**
```python
from dotenv import load_dotenv
import os
import pymysql

load_dotenv()  # .env 파일 읽기

conn = pymysql.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    db=os.getenv('DB_NAME'),
    charset='utf8mb4'
)
```

**보안 이점:**
- DB 접속 정보를 코드에서 분리
- 환경별 설정 관리 용이
- `.env` 파일을 `.gitignore`에 추가하여 버전 관리에서 제외

## 📚 9. 자주 사용하는 SQL 명령어 정리

### **데이터베이스 관리**
```sql
CREATE DATABASE test_db;      -- DB 생성
USE test_db;                  -- DB 선택
SHOW DATABASES;               -- DB 목록 조회
SHOW TABLES;                  -- 테이블 목록 조회
DESC table_name;              -- 테이블 구조 확인
```

### **데이터 조작**
```sql
-- 조회
SELECT * FROM table_name;
SELECT column1, column2 FROM table_name WHERE condition;

-- 삽입
INSERT INTO table_name (column1, column2) VALUES (value1, value2);

-- 수정
UPDATE table_name SET column1 = value1 WHERE condition;

-- 삭제
DELETE FROM table_name WHERE condition;
DROP TABLE table_name;  -- 테이블 삭제
```

## 🎯 10. 다음 학습 방향

### **우선순위 1: 고급 SQL**
- [ ] JOIN (INNER, LEFT, RIGHT, FULL)
- [ ] 집계 함수 (COUNT, SUM, AVG, MAX, MIN)
- [ ] GROUP BY, HAVING
- [ ] 서브쿼리 (Subquery)

### **우선순위 2: 실무 활용**
- [ ] 인덱스 최적화
- [ ] 트랜잭션 처리
- [ ] 저장 프로시저
- [ ] Python/Django ORM 연동

**💡 핵심 요약**

* SQL은 단순한 문법 암기가 아니라 **데이터베이스 관계형 구조와 제약조건을 이해**하는 것이 가장 중요
* 실습을 통해 외래키 제약조건의 중요성과 데이터 삽입/삭제의 올바른 순서를 먼저 파악해야 함을 깨달음
