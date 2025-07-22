# app/services/email_utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_confirmation_email(to_email: str, username: str, password: str, token: str):
    subject = "Confirmação de Cadastro - Sistema de Avaliação IA"
    verification_link = f"http://localhost:8001/auth/verify-email?token={token}"

    body = f"""\
Olá, {username}!

Sua conta foi criada com sucesso.

🔐 Login: {username}
🔑 Senha: {password}

Para ativar sua conta, clique no link abaixo:
🔗 {verification_link}

Se você não solicitou este cadastro, ignore este e-mail.

Atenciosamente,
Equipe do Sistema de Avaliação IA
"""
 # Monta a mensagem
    message = MIMEMultipart()
    message["From"] = SMTP_USER
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Envia via SMTP
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(message)
            print(f"✅ E-mail enviado para {to_email}")
    except Exception as e:
        print(f"🚫 Erro ao enviar e-mail para {to_email}: {e}")