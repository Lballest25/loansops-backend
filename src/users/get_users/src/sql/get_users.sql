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
    is_active = %(is_active)s
    AND (%(role)s IS NULL OR role = %(role)s)
ORDER BY
    created_at DESC
LIMIT  %(limit)s
OFFSET %(offset)s;
