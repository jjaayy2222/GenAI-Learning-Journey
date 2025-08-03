-- schema.sql

-- ---------------------
-- DB 초기화 및 테이블 생성
-- 데이터 생성 및 삽입
-- ---------------------

-- 고객 테이블 생성
CREATE TABLE TB_CUSTOMERS (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL
);

-- 제품 테이블 생성
CREATE TABLE TB_PRODUCTS (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL
);

-- 주문 상태 테이블 생성
CREATE TABLE TB_ORDER_STATUS (
    status_id INT AUTO_INCREMENT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL
);

-- 주문 테이블 생성
CREATE TABLE TB_ORDERS (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id INT NOT NULL,
    status_id INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES TB_CUSTOMERS(customer_id),
    FOREIGN KEY (status_id) REFERENCES TB_ORDER_STATUS(status_id)
);

-- 주문 상세 테이블 생성
CREATE TABLE TB_ORDER_ITEMS (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES TB_ORDERS(order_id),
    FOREIGN KEY (product_id) REFERENCES TB_PRODUCTS(product_id)
);

-- -------------------------------
-- 샘플 데이터 삽입
-- -------------------------------

-- 고객
INSERT INTO TB_CUSTOMERS (customer_name) VALUES 
('홍길동'), 
('김철수'), 
('이영희');

-- 제품
INSERT INTO TB_PRODUCTS (product_name) VALUES 
('사과'), 
('바나나'), 
('오렌지'), 
('포도');

-- 주문 상태
INSERT INTO TB_ORDER_STATUS (status_name) VALUES 
('주문접수'), 
('배송중'), 
('배송완료');

-- 기본 주문 2건
INSERT INTO TB_ORDERS (order_date, customer_id, status_id) VALUES 
('2025-08-01', 1, 1), 
('2025-08-02', 3, 3);

-- 주문 상세
INSERT INTO TB_ORDER_ITEMS (order_id, product_id, quantity) VALUES 
(1, 1, 3),  -- 사과
(1, 2, 2),  -- 바나나
(2, 3, 1),  -- 오렌지
(2, 4, 4);  -- 포도

-- 🔽 order_id = 1001 만들기

-- AUTO_INCREMENT 수동 설정
ALTER TABLE TB_ORDERS AUTO_INCREMENT = 1001;

-- 1001번 주문 추가
INSERT INTO TB_ORDERS (order_date, customer_id, status_id)
VALUES ('2025-08-03', 2, 2);  -- 김철수, 배송중

-- 1001번 주문 상세 추가
INSERT INTO TB_ORDER_ITEMS (order_id, product_id, quantity) VALUES 
(1001, 1, 2),   -- 사과
(1001, 4, 1);   -- 포도