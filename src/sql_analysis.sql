-- 1. Top 5 customers by total revenue
SELECT 
    name, 
    SUM(amount) as total_revenue
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id
WHERE status = 'Completed' -- Assuming only completed orders count as revenue
GROUP BY name
ORDER BY total_revenue DESC
LIMIT 5;

-- 2. Countries with highest unpaid orders count
SELECT 
    country, 
    COUNT(order_id) as unpaid_orders_count
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id
WHERE status IN ('Pending', 'Cancelled') -- Defining unpaid as Pending or Cancelled for this query
GROUP BY country
ORDER BY unpaid_orders_count DESC;

-- 3. Monthly revenue trend
SELECT 
    strftime('%Y-%m', order_date) as month, 
    SUM(amount) as revenue
FROM orders
WHERE status = 'Completed'
GROUP BY month
ORDER BY month;

-- 4. Customers with more than 3 completed orders
SELECT 
    name,
    COUNT(order_id) as completed_orders
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id
WHERE status = 'Completed'
GROUP BY name
HAVING completed_orders > 3;

-- 5. Orders paid later than 7 days
-- Assuming we have a 'payments' table or joined view. 
-- For this SQL script, I'll assume we load the joined dataframe into a single table 'orders_full' 
-- or we have separate tables. Let's assume separate tables for 1-4, but for 5 we need the payment info.
SELECT 
    o.order_id, 
    julianday(p.payment_date) - julianday(o.order_date) as delay_days
FROM orders o
JOIN payments p ON o.order_id = p.order_id
WHERE delay_days > 7;
