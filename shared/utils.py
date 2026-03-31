import json
import os
import socket
import smtplib
from email.mime.text import MIMEText
from typing import Any, Dict, Tuple

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from twilio.rest import Client as TwilioClient

from shared.constants import (
    PRESIGNED_GET_EXPIRATION,
    PRESIGNED_PUT_EXPIRATION,
    STATUS_CREATED_SUCCESS,
    STATUS_SERVER_ERROR,
)

load_dotenv()


# ── HTTP Response ──────────────────────────────────────────────
def get_response_handler(
    status: int, response: Dict[str, Any]
) -> Dict[str, Any]:
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS, POST, GET, PUT, PATCH, DELETE",
            "Access-Control-Allow-Headers": (
                "Content-Type, X-Amz-Date, Authorization, "
                "X-Api-Key, X-Amz-Security-Token"
            ),
        },
        "body": json.dumps(response, default=str),
    }


# ── S3 Presigned URLs ──────────────────────────────────────────
def generate_presigned_put_url(
    s3_key: str,
    content_type: str = "application/octet-stream",
    expiration: int = PRESIGNED_PUT_EXPIRATION,
) -> Tuple[int, Dict[str, Any]]:
    """
    Generates a presigned PUT URL so the client can upload
    a file directly to S3 without going through Lambda.
    """
    try:
        s3 = boto3.client("s3")
        bucket = os.environ["BUCKET_DOCUMENTS"]
        url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": bucket,
                "Key": s3_key,
                "ContentType": content_type,
            },
            ExpiresIn=expiration,
        )
        return STATUS_CREATED_SUCCESS, {
            "upload_url": url,
            "s3_key": s3_key,
            "expires_in": expiration,
        }
    except ClientError as exc:
        return STATUS_SERVER_ERROR, {"message": str(exc)}


def generate_presigned_get_url(
    s3_key: str,
    expiration: int = PRESIGNED_GET_EXPIRATION,
) -> Tuple[int, Dict[str, Any]]:
    """
    Generates a presigned GET URL so the client can download
    a file directly from S3.
    """
    try:
        s3 = boto3.client("s3")
        bucket = os.environ["BUCKET_DOCUMENTS"]
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": s3_key},
            ExpiresIn=expiration,
        )
        return STATUS_CREATED_SUCCESS, {
            "download_url": url,
            "s3_key": s3_key,
            "expires_in": expiration,
        }
    except ClientError as exc:
        return STATUS_SERVER_ERROR, {"message": str(exc)}


# ── Email ──────────────────────────────────────────────────────
def send_email(
    recipients: list,
    subject: str,
    template_path: str,
    data: Dict[str, Any],
) -> Tuple[int, Dict[str, Any]]:
    """
    Sends an HTML email via Gmail SMTP.

    Environment Variables:
        SENDER_EMAIL: Gmail address of the sender.
        SENDER_PASSWORD: App password of the sender.
    """
    try:
        smtp_host = "smtp.gmail.com"
        smtp_port = 465
        smtp_ipv4 = socket.getaddrinfo(
            smtp_host, smtp_port, socket.AF_INET
        )[0][4][0]
        sender_email = os.environ["SENDER_EMAIL"]
        sender_password = os.environ["SENDER_PASSWORD"]

        html_content = load_html_template(template_path, data)
        msg = MIMEText(html_content, "html")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = ", ".join(recipients)

        with smtplib.SMTP_SSL(smtp_ipv4, smtp_port) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, recipients, msg.as_string())

        return STATUS_CREATED_SUCCESS, {"message": "Email sent successfully"}
    except Exception as exc:
        return STATUS_SERVER_ERROR, {"message": str(exc)}


# ── WhatsApp (Twilio) ──────────────────────────────────────────
def send_whatsapp(
    to_number: str, body: str
) -> Tuple[int, Dict[str, Any]]:
    """
    Sends a WhatsApp message via Twilio.

    to_number must be in E.164 format, e.g. '+50688889999'.

    Environment Variables:
        TWILIO_ACCOUNT_SID
        TWILIO_AUTH_TOKEN
        TWILIO_WHATSAPP_FROM  e.g. 'whatsapp:+14155238886'
    """
    try:
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        from_number = os.environ["TWILIO_WHATSAPP_FROM"]

        client = TwilioClient(account_sid, auth_token)
        message = client.messages.create(
            from_=from_number,
            to=f"whatsapp:{to_number}",
            body=body,
        )
        return STATUS_CREATED_SUCCESS, {
            "message": "WhatsApp sent successfully",
            "sid": message.sid,
        }
    except Exception as exc:
        return STATUS_SERVER_ERROR, {"message": str(exc)}


# ── HTML Template Loader ───────────────────────────────────────
def load_html_template(template_path: str, data: Dict[str, Any]) -> str:
    with open(template_path, "r", encoding="utf-8") as file:
        html = file.read()
        for key, value in data.items():
            html = html.replace(f"{{{{{key}}}}}", str(value))
        return html
