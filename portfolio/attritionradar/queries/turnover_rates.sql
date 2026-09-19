SELECT e.department,e.job_level,COUNT(*) employees,
SUM(CASE WHEN x.exit_reason='voluntary' THEN 1 ELSE 0 END) voluntary_exits,
AVG(CASE WHEN x.exit_reason='voluntary' THEN 1.0 ELSE 0.0 END) voluntary_turnover_rate
FROM employees e LEFT JOIN exits x USING(employee_id)
GROUP BY e.department,e.job_level
ORDER BY voluntary_turnover_rate DESC;