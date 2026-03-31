SELECT
    user_id,
    user_name,
    email,
    identification,
    role,
    is_active,
    created_at
FROM
    users
WHERE
    email = %(email)s
    AND is_active = 1
LIMIT 1;
