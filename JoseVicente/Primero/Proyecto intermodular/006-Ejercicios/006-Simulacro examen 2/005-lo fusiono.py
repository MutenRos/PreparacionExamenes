import mysql.connector
from flask import Flask

aplicacion = Flask(__name__)

conexion = mysql.connector.connect(
  host="localhost",
  user="portafolio",
  password="portafolio",
  database="portafolio"
)

@aplicacion.route("/")
def raiz():
  cursor = conexion.cursor() 
  cursor.execute("SELECT * FROM portafolio;")
  cadena = '''
    <!docytpe html>
<html>
  <head>
    <style>
      body{
        background:DarkSlateGray;
        color:LightGray;
        font-family:sans-serif;
      }
      header,footer,main{
        width:800px;
        margin:auto;
        text-align:center;
        padding:20px;
      }
      main{
        display:grid;
        grid-template-columns:auto auto auto auto;
        gap:20px;
      }
      main img{
        width:100%;
        border:2px solid white;
        box-shadow:0px 10px 20px rgba(0,0,0,0.3);
      }
    </style>
  </head>
  <body>
    <header>
      <h1>Jose Vicente Carratala</h1>
      <h2>Portafolio</h2>
    </header>
    <main>
  '''
  
  lineas = cursor.fetchall()
  for linea in lineas:
    cadena += '''
      <article>
        <h3>'''+str(linea[1])+'''</h3>
        <p>'''+str(linea[2])+'''</p>
        <img src="'''+str(linea[3])+'''">
      </article>
    '''
  
  cadena += '''
    </main>
    <footer>
    </footer>
    <style>
      #contienemodal{
        position:fixed;
        top:0px;
        left:0px;
        width:100%;
        height:100%;
        background:rgba(0,0,0,0.6);
        display:none;
        justify-content:center;
        align-items:center;
        
      }
      #modal{
        width:400px;
        height:300px;
        text-align:center;
        padding:20px;
        background:white;
        display:flex;
        justify-content:center;
        align-items:center;
        border-radius:10px;
        box-shadow:0px 10px 20px black;
      }
    </style>
    <div id="contienemodal">
      <div id="modal">
        <img src="images.jpeg">
      </div>
    </div>
    <script>
      let imagenes = document.querySelectorAll("img")
      imagenes.forEach(function(imagen){
        imagen.onclick = function(){
          document.querySelector("#contienemodal").style.display = "flex"
        }
      })
    </script>
  </body>
</html>
  '''
  return cadena
  
if __name__ == "__main__":
  aplicacion.run()
