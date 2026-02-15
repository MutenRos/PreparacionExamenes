import sqlite3
def crear_tabla():
    '''
    Crea la tabla 'clientes' en la base de datos si no existe.
    No tiene parámetros ni retorna valores.
    '''
    basededatos = sqlite3.connect('clientes.db')
    cursor = basededatos.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        edad INTEGER NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    ''')    
    basededatos.commit()