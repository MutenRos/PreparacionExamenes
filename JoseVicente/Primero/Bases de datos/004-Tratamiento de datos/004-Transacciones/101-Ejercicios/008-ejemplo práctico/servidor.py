import mysql.connector
import json
from flask import Flask,render_template

aplicacion = Flask(__name__)

conexion = mysql.connector.connect(
  host="localhost",
  user="tiendaonline2526",
  password="tiendaonline2526",
  database="tiendaonline2526"
)

cursor = conexion.cursor(dictionary=True) 

@aplicacion.route("/")
def raiz():
  return render_template("index.html")
  
@aplicacion.route("/api")
def api():
  cursor.execute("SHOW TABLES;")

  tablas = cursor.fetchall()
  documento = {}
  for tabla in tablas:
    
    # Select * FROM cada una de las tablas
    cursor.execute("SELECT * FROM "+tabla['Tables_in_tiendaonline2526']+";")
    registros = cursor.fetchall()
    documento[tabla['Tables_in_tiendaonline2526']] = registros

  documento_json = json.dumps(documento, indent=4, ensure_ascii=False, default=str)
  return documento_json
  
@aplicacion.route("/admin")
def admin():
  return render_template("admin.html")
  
if __name__ == "__main__":
  aplicacion.run()
