import sqlite3

basededatos = sqlite3.connect("empresa.db")
cursor = basededatos.cursor()
while True:
  # Pantalla de selección de entidad ############################

  print("\033[2J")  # Borrar pantalla
  print("\033[0;0H", end="")
  print("Programa de gestión")
  print("Selecciona una entidad:")

  cursor.execute('''
    SELECT name 
    FROM sqlite_master 
    WHERE type='table'
    ORDER BY name;
    ''')
  contador = 1
  filas = cursor.fetchall()
  tabla = ""
  tablas = [0]
  for fila in filas:
    print(str(contador)+"-"+fila[0])
    contador += 1
    tablas.append(fila[0])
  opcion = input("Tu opción elegida: ")
  tabla = tablas[int(opcion)]

  # Pantalla de selección de operación ############################

  print("\033[2J")  # Borrar pantalla
  print("\033[0;0H", end="")
  print("La tabla seleccionada es: "+tabla)
  print("Selecciona una operación: ")
  print("1.-Crear un registro")
  print("2.-Listado de registros")
  print("3.-Actualizar un registro")
  print("4.-Eliminar un registro")
  opcion = int(input("Selecciona una opcion: "))

  # Pantalla de operación ############################

  print("\033[2J")  # Borrar pantalla
  print("\033[0;0H", end="")
  if opcion == 1:
    print("Insertamos un registro nuevo")
    cursor.execute('''
      PRAGMA table_info('''+tabla+''');
      ''')
    filas = cursor.fetchall()
    columnas = []
    for fila in filas:
      columnas.append(input("Introduce nuevo dato para "+fila[1]+": "))
    print(columnas)
    nombres_columnas = [f[1] for f in filas]

    # INSERT dinámico con placeholders
    placeholders = ",".join(["?"] * len(nombres_columnas))
    sql = f"INSERT INTO {tabla} ({','.join(nombres_columnas)}) VALUES ({placeholders})"

    cursor.execute(sql, columnas)
    basededatos.commit()
    print("Registro insertado.")
  elif opcion == 2:
    print("Listamos los registros")
  elif opcion == 3:
    print("Actualizamos un registro")
  elif opcion == 4:
    print("Eliminamos un registro")
  
  
  
  
  
  
  
