INSERT INTO loans (
    loan_id,
    user_id,
    amount,
    interest_rate,
    start_date,
    due_date,
    next_payment_date,
    status,
    created_by,
    updated_by
)
VALUES (
    %(loan_id)s,
    %(user_id)s,
    %(amount)s,
    %(interest_rate)s,
    %(start_date)s,
    %(due_date)s,
    %(next_payment_date)s,
    'PENDING',
    %(created_by)s,
    %(updated_by)s
);
