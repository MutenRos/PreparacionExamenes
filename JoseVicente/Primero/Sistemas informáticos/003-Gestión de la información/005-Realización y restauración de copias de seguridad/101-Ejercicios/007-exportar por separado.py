#!/usr/bin/env python3
import os
import json
import subprocess
import tarfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# ---------- PARÁMETROS DENTRO DEL CÓDIGO ----------

# Ruta del archivo de configuración con las credenciales
CONFIG_FILE = "config_mysql_backup.json"

# Carpeta donde se guardarán los backups (parámetro fijo dentro del código)
BACKUP_DIR = "/home/josevicente/backups/"

# Prefijo del nombre de los archivos de backup
BACKUP_PREFIX = "mysql_all_databases"

# --------------------------------------------------


# ===== UTILIDADES BÁSICAS =====

def load_config(config_path: str) -> Dict:
    """Carga el archivo JSON de configuración."""
    config_path = os.path.expanduser(config_path)
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_backup_dir(backup_dir: str) -> Path:
    """Crea la carpeta de backup si no existe y devuelve el Path."""
    path = Path(os.path.expanduser(backup_dir))
    path.mkdir(parents=True, exist_ok=True)
    return path


def print_header(title: str) -> None:
    """Imprime un encabezado simple en consola."""
    print("=" * 70)
    print(title)
    print("=" * 70)


def print_progress(current: int, total: int, db_name: str) -> None:
    """Imprime una barra de progreso sencilla en la misma línea."""
    bar_length = 40
    fraction = current / total if total > 0 else 1.0
    filled = int(bar_length * fraction)

    bar = "█" * filled + "-" * (bar_length - filled)
    percent = fraction * 100

    msg = f"[{bar}] {current}/{total} ({percent:5.1f}%) -> {db_name}"
    print("\r" + msg, end="", flush=True)


# ===== FUNCIONES ESPECÍFICAS DE MYSQL =====

def get_databases(config: Dict) -> List[str]:
    """
    Obtiene el listado de bases de datos usando el cliente 'mysql'.
    Equivalente conceptual a 'SHOW DATABASES;'.
    """
    mysql_conf = config["mysql"]
    mysql_path = config.get("mysql_path", "mysql")

    host = mysql_conf.get("host", "localhost")
    port = str(mysql_conf.get("port", 3306))
    user = mysql_conf["user"]
    password = mysql_conf["password"]

    cmd = [
        mysql_path,
        f"--host={host}",
        f"--port={port}",
        f"--user={user}",
        f"--password={password}",
        "-e",
        "SHOW DATABASES;"
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Error al obtener el listado de bases de datos.\nSTDERR:\n{result.stderr}"
        )

    lines = result.stdout.strip().splitlines()
    # Primera línea suele ser 'Database'
    databases = [line.strip() for line in lines[1:] if line.strip()]

    return databases


def dump_database(config: Dict, db_name: str, output_path: Path) -> None:
    """
    Realiza el volcado de una base de datos concreta a un archivo .sql (sin comprimir).
    Utiliza mysqldump y guarda el contenido directamente en el fichero.
    """
    mysql_conf = config["mysql"]
    mysqldump_path = config.get("mysqldump_path", "mysqldump")

    host = mysql_conf.get("host", "localhost")
    port = str(mysql_conf.get("port", 3306))
    user = mysql_conf["user"]
    password = mysql_conf["password"]

    cmd = [
        mysqldump_path,
        f"--host={host}",
        f"--port={port}",
        f"--user={user}",
        f"--password={password}",
        "--single-transaction",
        "--quick",
        "--force",  # Intentar continuar aunque haya errores (vistas rotas, etc.)
        db_name
    ]

    with open(output_path, "wb") as f:
        process = subprocess.run(
            cmd,
            stdout=f,
            stderr=subprocess.PIPE
        )

    if process.returncode != 0:
        # No borramos el archivo para poder inspeccionarlo si hace falta,
        # pero informamos del error.
        stderr = process.stderr.decode("utf-8", errors="ignore")
        raise RuntimeError(
            f"mysqldump falló para la BD '{db_name}' "
            f"con código {process.returncode}.\nError:\n{stderr}"
        )


def create_master_archive(sql_files: List[Path], backup_dir: Path,
                          prefix: str, timestamp: str) -> Path:
    """
    Crea un archivo maestro comprimido (.tar.gz) que contiene todos
    los ficheros .sql generados.
    """
    master_name = f"{prefix}_ALL_{timestamp}.tar.gz"
    master_path = backup_dir / master_name

    with tarfile.open(master_path, "w:gz") as tar:
        for sql_file in sql_files:
            # Guardamos en el tar solo el nombre del fichero, sin la ruta completa
            tar.add(sql_file, arcname=sql_file.name)

    return master_path


# ===== FUNCIÓN PRINCIPAL =====

def main():
    # 1. Cargar configuración
    print_header("COPIA DE SEGURIDAD DE TODAS LAS BASES DE DATOS MySQL")
    config = load_config(CONFIG_FILE)

    # 2. Asegurar carpeta de backup
    backup_dir = ensure_backup_dir(BACKUP_DIR)
    print(f"Carpeta de backups: {backup_dir}")

    # 3. Generar una marca de tiempo única para toda la ejecución
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 4. Obtener listado de bases de datos
    print("\nObteniendo listado de bases de datos...")
    databases = get_databases(config)

    if not databases:
        print("No se han encontrado bases de datos.")
        return

    total = len(databases)
    print(f"Se han encontrado {total} bases de datos:")
    for db in databases:
        print(f"  - {db}")

    print("\nIniciando volcados individuales...\n")

    dump_files: List[Path] = []
    failed: List[str] = []

    # 5. Volcar cada base de datos con una barra de progreso
    for i, db_name in enumerate(databases, start=1):
        # Actualizamos barra de progreso
        print_progress(i, total, db_name)

        # Nombre de fichero específico para cada BD
        sql_filename = f"{BACKUP_PREFIX}_{db_name}_{timestamp}.sql"
        sql_path = backup_dir / sql_filename

        try:
            dump_database(config, db_name, sql_path)
            dump_files.append(sql_path)
        except RuntimeError as e:
            # Cerramos la barra de progreso actual con salto de línea
            print()
            print(f"[ERROR] Falló el backup de la base de datos '{db_name}':")
            print(e)
            failed.append(db_name)

    # Aseguramos que la barra de progreso termina en una línea limpia
    print()

    # 6. Crear archivo maestro comprimido con todos los .sql generados
    if dump_files:
        print("\nCreando archivo maestro comprimido con todos los .sql...")
        master_path = create_master_archive(dump_files, backup_dir, BACKUP_PREFIX, timestamp)
        print(f"Archivo maestro creado: {master_path}")
    else:
        print("\nNo se han generado archivos .sql válidos. No se creará archivo maestro.")
        master_path = None

    # 7. Resumen final
    print_header("RESUMEN DEL BACKUP")
    print(f"Total de bases de datos encontradas: {total}")
    print(f"Backups realizados correctamente : {len(dump_files)}")
    print(f"Backups con errores            : {len(failed)}")

    if dump_files:
        print("\nFicheros .sql generados:")
        for p in dump_files:
            print(f"  - {p}")

    if failed:
        print("\nBases de datos con errores de volcado:")
        for db in failed:
            print(f"  - {db}")

    if master_path is not None:
        print(f"\nArchivo maestro (.tar.gz) con todos los .sql:")
        print(f"  - {master_path}")

    print("\nProceso de copia de seguridad finalizado.")


if __name__ == "__main__":
    main()

