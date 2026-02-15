#!/usr/bin/env python3
import os
import sys
import json
import gzip
import subprocess
from datetime import datetime
from pathlib import Path

# ---------- PARÁMETROS DENTRO DEL CÓDIGO ----------

# Ruta del archivo de configuración con las credenciales
CONFIG_FILE = "config_mysql_backup.json"

# Carpeta donde se guardarán los backups (parámetro fijo dentro del código)
BACKUP_DIR = "/home/josevicente/backups/"

# Prefijo del nombre del archivo de backup
BACKUP_PREFIX = "mysql_all_databases"

# --------------------------------------------------


def load_config(config_path: str) -> dict:
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


def build_backup_filename(prefix: str, backup_dir: Path) -> Path:
    """Genera un nombre de archivo con fecha y hora."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.sql.gz"
    return backup_dir / filename


def run_mysqldump_all(config: dict, output_path: Path) -> None:
    """
    Ejecuta mysqldump para todas las bases de datos y guarda
    la salida comprimida en GZIP.

    Se usa --force para que continúe aunque haya errores en
    alguna vista/tabla (por ejemplo, una vista inválida).
    """

    mysql_conf = config["mysql"]
    mysqldump_path = config.get("mysqldump_path", "mysqldump")

    host = mysql_conf.get("host", "localhost")
    port = str(mysql_conf.get("port", 3306))
    user = mysql_conf["user"]
    password = mysql_conf["password"]

    # Comando mysqldump para todas las bases de datos
    cmd = [
        mysqldump_path,
        f"--host={host}",
        f"--port={port}",
        f"--user={user}",
        f"--password={password}",
        "--all-databases",
        "--single-transaction",
        "--quick",
        "--force",  # <-- seguir aunque haya errores en vistas/tablas
    ]

    # Ejecutamos mysqldump y vamos leyendo el STDOUT en streaming,
    # escribiéndolo directamente en un archivo .gz para no cargar
    # toda la copia en memoria.
    with gzip.open(output_path, "wb") as gz_file:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if not process.stdout:
            raise RuntimeError("No se pudo obtener la salida de mysqldump")

        # Leer en bloques para no consumir demasiada memoria
        for chunk in iter(lambda: process.stdout.read(4096), b""):
            gz_file.write(chunk)

        process.stdout.close()
        stderr = process.stderr.read().decode("utf-8", errors="ignore")
        process.stderr.close()
        retcode = process.wait()

        # Con --force puede seguir habiendo código de salida != 0.
        # No borramos el fichero: solo avisamos.
        if retcode != 0:
            msg = (
                f"AVISO: mysqldump terminó con código {retcode}.\n"
                "Es posible que alguna vista/tabla no se haya exportado correctamente.\n"
                "Mensaje de error de mysqldump:\n"
                f"{stderr}"
            )
            print(msg, file=sys.stderr)


def main():
    try:
        # 1. Cargar configuración
        config = load_config(CONFIG_FILE)

        # 2. Asegurar carpeta de backup (parámetro fijo en el código)
        backup_dir = ensure_backup_dir(BACKUP_DIR)

        # 3. Construir nombre de archivo
        backup_file = build_backup_filename(BACKUP_PREFIX, backup_dir)

        # 4. Ejecutar mysqldump y guardar la copia comprimida
        print("Iniciando backup de todas las bases de datos MySQL...")
        print(f"Archivo de salida: {backup_file}")

        run_mysqldump_all(config, backup_file)

        print("Proceso de backup finalizado (revisa posibles avisos en la salida de error).")

    except Exception as e:
        print(f"Error durante el backup: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

