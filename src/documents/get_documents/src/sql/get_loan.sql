SELECT loan_id, user_id
FROM   loans
WHERE  loan_id = %(loan_id)s
LIMIT 1;
