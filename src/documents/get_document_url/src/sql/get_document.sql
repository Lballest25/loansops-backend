SELECT
    document_id,
    loan_id,
    uploaded_by,
    s3_key,
    document_type,
    created_at
FROM
    documents
WHERE
    document_id = %(document_id)s
    AND loan_id = %(loan_id)s
LIMIT 1;
