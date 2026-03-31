INSERT INTO documents (
    document_id,
    loan_id,
    uploaded_by,
    s3_key,
    document_type
)
VALUES (
    %(document_id)s,
    %(loan_id)s,
    %(uploaded_by)s,
    %(s3_key)s,
    %(document_type)s
);
