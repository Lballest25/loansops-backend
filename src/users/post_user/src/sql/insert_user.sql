INSERT INTO users (
    user_name,
    email, 
    identification,
    role, 
    created_by, 
    updated_by
)
VALUES (
    %(user_name)s,
    %(email)s,
    %(identification)s,
    %(role)s,
    %(created_by)s,
    %(updated_by)s
);
