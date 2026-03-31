-- =============================================================
-- LoanOps – Database Schema
-- Engine: MySQL 8.x  |  Charset: utf8mb4
-- Run manually on RDS before first deploy.
-- =============================================================

CREATE DATABASE IF NOT EXISTS loansops
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE loansops;

-- -------------------------------------------------------------
-- users
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id         VARCHAR(36)                             NOT NULL,
    user_name       VARCHAR(255)                            NOT NULL,
    email           VARCHAR(255)                            NOT NULL,
    identification  VARCHAR(50)                             NOT NULL,
    role            ENUM('ADMIN','ANALYST','CLIENT')        NOT NULL,
    is_active       TINYINT(1)      DEFAULT 1               NOT NULL,
    created_at      TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    created_by      VARCHAR(36),
    updated_at      TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
                    ON UPDATE CURRENT_TIMESTAMP,
    updated_by      VARCHAR(36),
    CONSTRAINT pk_users            PRIMARY KEY (user_id),
    CONSTRAINT uq_users_email      UNIQUE (email),
    CONSTRAINT uq_users_ident      UNIQUE (identification)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------------
-- loans
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS loans (
    loan_id             VARCHAR(36)                                             NOT NULL,
    user_id             VARCHAR(36)                                             NOT NULL,
    amount              DECIMAL(15,2)                                           NOT NULL,
    interest_rate       DECIMAL(5,2)                                            NOT NULL,
    start_date          DATE                                                    NOT NULL,
    due_date            DATE                                                    NOT NULL,
    next_payment_date   DATE,
    status              ENUM('PENDING','ACTIVE','PAID','OVERDUE','CANCELLED')
                        DEFAULT 'PENDING'                                       NOT NULL,
    created_at          TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    created_by          VARCHAR(36),
    updated_at          TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,
    updated_by          VARCHAR(36),
    CONSTRAINT pk_loans             PRIMARY KEY (loan_id),
    CONSTRAINT fk_loans_user        FOREIGN KEY (user_id)
        REFERENCES users (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------------
-- documents
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS documents (
    document_id     VARCHAR(36)                                                         NOT NULL,
    loan_id         VARCHAR(36)                                                         NOT NULL,
    uploaded_by     VARCHAR(36)                                                         NOT NULL,
    s3_key          VARCHAR(500)                                                        NOT NULL,
    document_type   ENUM('PAYMENT_RECEIPT','CONTRACT','ID_VERIFICATION','OTHER')        NOT NULL,
    created_at      TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_documents         PRIMARY KEY (document_id),
    CONSTRAINT fk_documents_loan    FOREIGN KEY (loan_id)
        REFERENCES loans (loan_id),
    CONSTRAINT fk_documents_user    FOREIGN KEY (uploaded_by)
        REFERENCES users (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
