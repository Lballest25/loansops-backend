SELECT
    l.loan_id,
    l.user_id,
    u.user_name,
    u.email,
    u.phone,
    l.amount,
    l.interest_rate,
    l.next_payment_date,
    l.due_date
FROM
    loans l
    INNER JOIN users u ON u.user_id = l.user_id
WHERE
    l.status       = 'ACTIVE'
    AND l.next_payment_date = DATE_ADD(CURDATE(), INTERVAL %(days_before)s DAY)
    AND u.is_active = 1;
