SELECT
    d.document_id,
    d.loan_id,
    d.uploaded_by,
    u.user_name  AS uploaded_by_name,
    d.s3_key,
    d.document_type,
    d.created_at
FROM
    documents d
    INNER JOIN users u ON u.user_id = d.uploaded_by
WHERE
    d.loan_id = %(loan_id)s
ORDER BY
    d.created_at DESC;
