# LoanOps Backend

Backend serverless production-grade para la plataforma de gestión de préstamos **LoanOps**, construido sobre AWS con Python 3.12.

---

## Stack

| Capa | Tecnología |
|---|---|
| Runtime | Python 3.12 |
| Infraestructura | AWS Serverless Framework v4 |
| Cómputo | AWS Lambda |
| Base de datos | RDS MySQL 8.x (raw SQL, sin ORM) |
| Almacenamiento | S3 (presigned URLs) |
| Autenticación | AWS Cognito User Pools |
| Notificaciones | Gmail SMTP + Twilio WhatsApp |
| CI/CD | GitHub Actions |
| Calidad de código | Black · Flake8 · Pylint · MyPy |

---

## Estructura del proyecto

```
loansops-backend/
├── shared/                         # Código reutilizable entre funciones
│   ├── constants.py                # Roles, statuses, tipos de documento
│   ├── db_config.py                # Connection pool MySQL
│   ├── utils.py                    # Email, WhatsApp, presigned URLs
│   ├── decorators/
│   │   ├── user_session.py         # @user_session — valida JWT y carga usuario
│   │   ├── user_permission.py      # @user_permission(*roles) — valida rol
│   │   └── query_reader.py         # @sql_query_reader — carga archivos .sql
│   ├── queries/                    # Queries compartidas
│   └── templates/                  # Templates HTML para emails
│
├── src/
│   ├── users/                      # POST · GET list · GET by ID · PUT
│   ├── loans/                      # POST · GET list · GET by ID · PUT · PATCH status
│   ├── documents/                  # Presigned PUT URL · Presigned GET URL · GET list
│   ├── notifications/              # POST send (email + WhatsApp)
│   ├── cron/                       # Recordatorios de pago (EventBridge diario)
│   └── cognito/                    # Lambda interna — crea usuario en Cognito
│
├── layers/
│   ├── dependencies/python/        # Generado por build_layers.sh (pip packages)
│   └── shared/python/shared/       # Generado por build_layers.sh (módulo shared)
│
├── migrations/
│   └── schema.sql                  # DDL: users, loans, documents
│
├── scripts/
│   └── build_layers.sh             # Build de los Lambda Layers
│
├── .code_quality/                  # Configuración Black, Flake8, Pylint, MyPy
├── .github/workflows/              # CI/CD pipelines dev y prod
├── api-docs.yaml                   # OpenAPI 3.0 — documentación central
├── serverless.yml                  # Configuración principal Serverless Framework
├── requirements.txt                # Dependencias Python
└── .env.example                    # Variables de entorno de referencia
```

---

## Endpoints

### Users
| Método | Path | Roles |
|---|---|---|
| POST | `/users/register` | ADMIN |
| GET | `/users` | ADMIN, ANALYST |
| GET | `/users/{user_id}` | ADMIN, ANALYST, CLIENT (solo el propio) |
| PUT | `/users/{user_id}/update` | ADMIN |

### Loans
| Método | Path | Roles |
|---|---|---|
| POST | `/loans` | ADMIN, ANALYST |
| GET | `/loans/list` | ADMIN, ANALYST, CLIENT (solo los propios) |
| GET | `/loans/{loan_id}` | ADMIN, ANALYST, CLIENT (solo el propio) |
| PUT | `/loans/{loan_id}/update` | ADMIN, ANALYST |
| PATCH | `/loans/{loan_id}/status` | ADMIN |

### Documents
| Método | Path | Roles |
|---|---|---|
| POST | `/loans/{loan_id}/documents/upload-url` | Todos |
| GET | `/loans/{loan_id}/documents/{document_id}/download-url` | Todos |
| GET | `/loans/{loan_id}/documents` | Todos |

> Los archivos **nunca** pasan por Lambda. El cliente sube y descarga directamente desde S3 usando presigned URLs.

### Notifications
| Método | Path | Roles |
|---|---|---|
| POST | `/notifications/send` | ADMIN |

---

## Roles

| Rol | Descripción |
|---|---|
| `ADMIN` | Acceso total — gestión de usuarios, préstamos, notificaciones |
| `ANALYST` | Puede crear y consultar préstamos, no puede cambiar status ni gestionar usuarios |
| `CLIENT` | Solo puede ver sus propios préstamos y documentos |

---

## Base de datos

Ejecutar `migrations/schema.sql` en el RDS antes del primer deploy:

```bash
mysql -h <RDS_HOST> -u admin -p loansops < migrations/schema.sql
```

Tablas: `users` · `loans` · `documents`

---

## Configuración de variables de entorno

Copiar `.env.example` a `.env` para desarrollo local.

En AWS, todas las variables se leen desde **SSM Parameter Store** bajo el prefijo `/loansops/{stage}/`.

| Parámetro SSM | Descripción |
|---|---|
| `/loansops/{stage}/db/host` | Host del RDS |
| `/loansops/{stage}/db/user` | Usuario de la BD |
| `/loansops/{stage}/db/password` | Contraseña de la BD |
| `/loansops/{stage}/db/name` | Nombre de la BD |
| `/loansops/{stage}/s3/documents_bucket` | Nombre del bucket S3 |
| `/loansops/{stage}/cognito/user_pool_id` | ID del Cognito User Pool |
| `/loansops/{stage}/cognito/client_id` | ID del Cognito Client |
| `/loansops/{stage}/cognito/user_pool_arn` | ARN del Cognito User Pool |
| `/loansops/{stage}/lambda/create_cognito_user` | Nombre de la Lambda interna de Cognito |
| `/loansops/{stage}/email/sender` | Email remitente (Gmail) |
| `/loansops/{stage}/email/password` | App password de Gmail |
| `/loansops/{stage}/twilio/account_sid` | Twilio Account SID |
| `/loansops/{stage}/twilio/auth_token` | Twilio Auth Token |
| `/loansops/{stage}/twilio/whatsapp_from` | Número Twilio WhatsApp (ej. `whatsapp:+14155238886`) |

---

## Lambda Layers

El proyecto usa dos layers compartidos para reducir el tamaño de cada función:

| Layer | Contenido | Path en Lambda |
|---|---|---|
| `dependencies` | Paquetes de `requirements.txt` | `/opt/python/` |
| `shared` | Módulo `shared/` | `/opt/python/shared/` |

### Build local

```bash
bash scripts/build_layers.sh
```

> Agrega estas rutas al `.gitignore`:
> ```
> layers/dependencies/python/
> layers/shared/python/shared/
> ```

---

## Deploy

### Prerequisitos

```bash
npm install -g serverless
pip install -r requirements.txt
```

### Dev

```bash
bash scripts/build_layers.sh
serverless deploy --stage dev
```

### Prod

```bash
bash scripts/build_layers.sh
serverless deploy --stage prod
```

---

## CI/CD

| Branch | Pipeline | Ambiente |
|---|---|---|
| `develop` | `.github/workflows/dev.yml` | dev |
| `main` | `.github/workflows/prod.yml` | prod |

Cada pipeline ejecuta en orden:
1. **Static Analysis** — Black, Flake8, Pylint, MyPy
2. **Build Layers** — `bash scripts/build_layers.sh`
3. **Deploy** — `serverless deploy --stage {env}`

### Secrets requeridos en GitHub

| Secret | Ambiente |
|---|---|
| `AWS_ACCESS_KEY_ID` | dev |
| `AWS_SECRET_ACCESS_KEY` | dev |
| `AWS_ACCESS_KEY_ID_PROD` | prod |
| `AWS_SECRET_ACCESS_KEY_PROD` | prod |

---

## Cron — Recordatorios de pago

Un EventBridge rule dispara la función `paymentReminders` todos los días a las **9:00 AM UTC**.

Busca préstamos con `status = ACTIVE` cuyo `next_payment_date` sea exactamente **7 días** a partir de hoy y envía recordatorio por **email y WhatsApp** a cada cliente.

---

## Calidad de código

```bash
black --check --line-length 79 .
flake8 --config .code_quality/.flake8 .
pylint --rcfile .code_quality/.pylintrc shared/ src/
mypy --config-file .code_quality/mypy.ini shared/ src/
```
