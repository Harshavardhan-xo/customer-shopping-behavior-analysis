WITH activity AS (
    SELECT customer_id,MAX(event_date) last_event_date,COUNT(*) event_frequency,AVG(login_count) avg_logins
    FROM usage_events GROUP BY customer_id
), tickets AS (
    SELECT customer_id,COUNT(*) ticket_frequency FROM support_tickets GROUP BY customer_id
)
SELECT c.customer_id,c.plan_tier,c.mrr,c.industry,c.region,
       COALESCE(a.event_frequency,0) usage_frequency,
       COALESCE(a.avg_logins,0) avg_logins,
       COALESCE(t.ticket_frequency,0) ticket_frequency,
       COALESCE(CAST(julianday('now')-julianday(a.last_event_date) AS INTEGER),999) recency_days
FROM customers c
LEFT JOIN activity a USING(customer_id)
LEFT JOIN tickets t USING(customer_id);