WITH revenue AS (
SELECT s.sku_id,SUM(s.units_sold*k.unit_price) revenue
FROM daily_sales s JOIN skus k USING(sku_id)
WHERE date(s.date)>=date('now','-365 day')
GROUP BY s.sku_id),
ranked AS (
SELECT sku_id,revenue,CUME_DIST() OVER(ORDER BY revenue DESC) pct_rank FROM revenue)
SELECT sku_id,revenue,CASE WHEN pct_rank<=.20 THEN 'A' WHEN pct_rank<=.50 THEN 'B' ELSE 'C' END abc_tier
FROM ranked ORDER BY revenue DESC;