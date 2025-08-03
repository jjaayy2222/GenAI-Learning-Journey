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
    o.order_id = 1001 
GROUP BY  
    o.order_id, o.customer_id, o.order_date, s.status_name;