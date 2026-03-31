SELECT
    l.loan_id,
    l.user_id,
    u.user_name,
    u.email,
    l.amount,
    l.interest_rate,
    l.start_date,
    l.due_date,
    l.next_payment_date,
    l.status,
    l.created_at,
    l.created_by,
    l.updated_at,
    l.updated_by
FROM
    loans l
    INNER JOIN users u ON u.user_id = l.user_id
WHERE
    (%(user_id)s IS NULL OR l.user_id = %(user_id)s)
    AND (%(status)s  IS NULL OR l.status  = %(status)s)
ORDER BY
    l.created_at DESC
LIMIT  %(limit)s
OFFSET %(offset)s;
