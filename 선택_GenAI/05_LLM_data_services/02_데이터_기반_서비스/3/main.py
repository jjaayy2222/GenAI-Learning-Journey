from db import query_db
from tabulate import tabulate                                             # 결과를 표 형태로 보기 위해 사용

# 이전 코드 
# result = query_db("SELECT ... WHERE o.order_id = 1001 ...")
# print(result)

# 새 코드 
# 가독성 향상, 유지보수 편함
# 현재 DB에 존재하는 주문 ID (1003)에 맞게 수정
sql = """
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

result = query_db(sql)

# print(result)
# 결과를 표 형식으로 출력
if result:
    print(tabulate(result, headers="keys", tablefmt="grid"))
else:
    print("결과가 없습니다.")