SELECT
    user_id,
    user_name,
    email,
    role,
    is_active
FROM
    users
WHERE
    user_id = %(user_id)s
    AND is_active = 1
LIMIT 1;
