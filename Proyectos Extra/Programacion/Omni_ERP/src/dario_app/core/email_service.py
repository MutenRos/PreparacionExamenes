"""Email service for sending documents and notifications."""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import Optional
import os


class EmailService:
    """Service for sending emails with PDF attachments."""
    
    def __init__(self):
        """Initialize email service with configuration."""
        # Use environment variables or defaults
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "noreply@erpdario.com")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@erpdario.com")
        self.from_name = os.getenv("FROM_NAME", "ERP Dario")
    
    def send_invoice_email(
        self,
        to_email: str,
        customer_name: str,
        invoice_number: str,
        pdf_content: bytes,
        pdf_filename: str,
        organization_name: str = "ERP Dario"
    ) -> bool:
        """
        Send invoice PDF via email.
        
        Args:
            to_email: Recipient email address
            customer_name: Name of the customer
            invoice_number: Invoice number
            pdf_content: PDF file content as bytes
            pdf_filename: Name for the PDF attachment
            organization_name: Name of the organization sending the invoice
            
        Returns:
            True if email was sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = f"Factura {invoice_number} - {organization_name}"
            
            # Email body
            body = f"""
Estimado/a {customer_name},

Adjuntamos su factura {invoice_number}.

Detalles:
- Número de factura: {invoice_number}
- Empresa: {organization_name}

Si tiene alguna pregunta sobre esta factura, no dude en contactarnos.

Gracias por su preferencia.

---
{organization_name}
Este es un correo automático, por favor no responder.
            """
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Attach PDF
            pdf_attachment = MIMEApplication(pdf_content, _subtype='pdf')
            pdf_attachment.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
            msg.attach(pdf_attachment)
            
            # Send email
            if self.smtp_password:  # Only send if SMTP is configured
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_password)
                    server.send_message(msg)
                return True
            else:
                # If SMTP not configured, just log (for development)
                print(f"[EMAIL] Would send invoice {invoice_number} to {to_email}")
                print(f"[EMAIL] PDF filename: {pdf_filename}")
                print(f"[EMAIL] SMTP not configured - email not sent")
                return False
                
        except Exception as e:
            print(f"[EMAIL ERROR] Failed to send email: {str(e)}")
            return False
    
    def send_test_email(self, to_email: str) -> bool:
        """Send a test email to verify configuration."""
        try:
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = "Test Email - ERP Dario"
            
            body = "Este es un correo de prueba desde ERP Dario."
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            if self.smtp_password:
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_password)
                    server.send_message(msg)
                return True
            else:
                print("[EMAIL] SMTP not configured - test email not sent")
                return False
                
        except Exception as e:
            print(f"[EMAIL ERROR] Test email failed: {str(e)}")
            return False
