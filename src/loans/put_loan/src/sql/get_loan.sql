SELECT loan_id, status
FROM   loans
WHERE  loan_id = %(loan_id)s
LIMIT 1;
