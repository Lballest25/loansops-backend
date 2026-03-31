SELECT
    user_id,
    user_name,
    email,
    identification,
    role,
    is_active,
    created_at,
    created_by,
    updated_at,
    updated_by
FROM
    users
WHERE
    user_id = %(user_id)s
    AND is_active = 1
LIMIT 1;
