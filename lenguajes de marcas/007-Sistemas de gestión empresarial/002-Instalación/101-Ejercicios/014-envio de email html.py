import smtplib
from email.message import EmailMessage
import os

SMTP_SERVER = os.environ.get("EMAIL_SERVIDOR")
SMTP_PORT = 587          # 587 = STARTTLS, 465 = SSL
SMTP_USER = os.environ.get("EMAIL_USUARIO")
SMTP_PASS = os.environ.get("EMAIL_CONTRASENA")

msg = EmailMessage()
msg["From"] = "info@jocarsa.com"
msg["To"] = "jocarsa2@gmail.com"
msg["Subject"] = "Informe de notas"

# --- Plain text fallback (important) ---
msg.set_content(
    "Este correo contiene un informe de notas en formato HTML.\n"
    "Si no lo ves correctamente, por favor usa un cliente de correo compatible."
)

# --- HTML content ---
html_content = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <style>
      td,th{padding:5px;}
    </style>
  </head>
  <body>
    <table border="0" style="font-family:sans-serif;text-align:justify;">
      <tr>
        <td style="width:10%"></td>
        <td style="width:80%">
          <table border="0" width="100%">
            <tr>
              <td>
                <h1 style="text-align:center;">Informe de notas</h1>
                <p>
                  Este no es el boletín trimestral de notas
                  del centro de formación.<br>
                  Este es un informe de notas de profesor.<br>
                  Incluye las notas de las asignaturas:
                </p>
                <ul>
                  <li>Programación</li>
                  <li>Lenguajes de marcas</li>
                  <li>Bases de datos</li>
                  <li>Proyecto intermodular I</li>
                </ul>
              </td>
            </tr>
            <tr>
              <td>
                <table border="0" width="100%">
                  <tr style="background:indigo;color:white;">
                    <th>Módulo profesional</th>
                    <th>ACT</th>
                    <th>CONTROL</th>
                    <th>EVAL</th>
                    <th>COMP</th>
                    <th>TOT</th>
                  </tr>
                  <tr>
                    <td>Programación</td>
                    <td>8</td><td>8</td><td>8</td><td>8</td><td>8</td>
                  </tr>
                  <tr>
                    <td>Lenguajes de marcas</td>
                    <td>8</td><td>8</td><td>8</td><td>8</td><td>8</td>
                  </tr>
                  <tr>
                    <td>Bases de datos</td>
                    <td>8</td><td>8</td><td>8</td><td>8</td><td>8</td>
                  </tr>
                  <tr>
                    <td>Proyecto Intermodular</td>
                    <td>8</td><td>8</td><td>8</td><td>8</td><td>8</td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td>
                <h3 style="text-align:center;">Revisión de notas</h3>
                <p>
                  Quien quiera revisar calificaciones, mañana martes
                  27 de enero a las 11:15 (en el descanso)
                </p>
              </td>
            </tr>
          </table>
        </td>
        <td style="width:10%"></td>
      </tr>
    </table>
  </body>
</html>
"""

msg.add_alternative(html_content, subtype="html")

# --- Send email ---
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
    smtp.starttls()
    smtp.login(SMTP_USER, SMTP_PASS)
    smtp.send_message(msg)

print("Email sent")
