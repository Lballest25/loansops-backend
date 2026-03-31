UPDATE loans
SET
    status     = %(status)s,
    updated_by = %(updated_by)s
WHERE
    loan_id = %(loan_id)s;
