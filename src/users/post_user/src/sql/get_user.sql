SELECT
    user_id
FROM
    users
WHERE
    email = %(email)s
LIMIT 1;