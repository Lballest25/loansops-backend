SELECT user_id
FROM   users
WHERE  user_id = %(user_id)s
  AND  is_active = 1
LIMIT 1;
