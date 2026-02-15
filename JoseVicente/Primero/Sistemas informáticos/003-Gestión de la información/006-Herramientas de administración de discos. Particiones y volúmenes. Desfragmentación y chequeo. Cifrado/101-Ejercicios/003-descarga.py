import json
import os
import stat
import time
import datetime
import posixpath  # para rutas remotas tipo UNIX
import paramiko


# -------------------------------------------------
# Utilidades de formato
# -------------------------------------------------

def format_bytes(n: int) -> str:
    # Devuelve un string legible: 123.4 MB, etc.
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def format_time(seconds: float) -> str:
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h > 0:
        return f"{h:d}h {m:02d}m {s:02d}s"
    elif m > 0:
        return f"{m:d}m {s:02d}s"
    else:
        return f"{s:d}s"


# -------------------------------------------------
# Gestión de progreso global
# -------------------------------------------------

class GlobalProgress:
    def __init__(self, total_bytes: int):
        self.total_bytes = total_bytes
        self.transferred_bytes = 0
        self.start_time = time.time()

    def add(self, delta: int):
        self.transferred_bytes += delta
        self.print_progress()

    def print_progress(self):
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            speed = self.transferred_bytes / elapsed
        else:
            speed = 0.0

        if speed > 0:
            remaining = (self.total_bytes - self.transferred_bytes) / speed
        else:
            remaining = 0

        if self.total_bytes > 0:
            percent = (self.transferred_bytes / self.total_bytes) * 100.0
        else:
            percent = 0.0

        bar_len = 30
        filled = int(bar_len * percent / 100.0)
        bar = "█" * filled + "-" * (bar_len - filled)

        msg = (
            f"\r[{bar}] {percent:6.2f}% "
            f"| {format_bytes(self.transferred_bytes)}/{format_bytes(self.total_bytes)} "
            f"| elapsed {format_time(elapsed)} "
            f"| ETA {format_time(remaining)}"
        )
        print(msg, end="", flush=True)

        if self.transferred_bytes >= self.total_bytes:
            print()  # newline final


# -------------------------------------------------
# Conexión SSH/SFTP
# -------------------------------------------------

def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_ssh_client(cfg: dict) -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host = cfg["host"]
    port = cfg.get("port", 22)
    username = cfg["username"]
    auth = cfg.get("auth", {})
    auth_type = auth.get("type", "password")

    if auth_type == "password":
        password = auth["password"]
        client.connect(hostname=host, port=port, username=username, password=password)
    elif auth_type == "key":
        key_filename = auth["key_filename"]
        passphrase = auth.get("passphrase")
        client.connect(
            hostname=host,
            port=port,
            username=username,
            key_filename=key_filename,
            passphrase=passphrase,
        )
    else:
        raise ValueError(f"Unsupported auth type: {auth_type}")

    return client


# -------------------------------------------------
# Recorrido remoto y descarga
# -------------------------------------------------

def collect_remote_files(sftp: paramiko.SFTPClient, root_path: str):
    """
    Devuelve una lista de (ruta_remota, tamaño_en_bytes) para todos
    los ficheros bajo root_path.
    """
    files = []

    def _walk(path: str):
        try:
            entries = sftp.listdir_attr(path)
        except IOError as e:
            print(f"\n[ERROR] No se pudo listar {path}: {e}")
            return

        for entry in entries:
            name = entry.filename
            if name in (".", ".."):
                continue

            remote_path = posixpath.join(path, name)

            if stat.S_ISDIR(entry.st_mode):
                _walk(remote_path)
            else:
                files.append((remote_path, entry.st_size))

    _walk(root_path)
    return files


def download_with_progress(
    sftp: paramiko.SFTPClient,
    files,
    root_path: str,
    local_base: str,
):
    # Tamaño total
    total_bytes = sum(size for _, size in files)
    progress = GlobalProgress(total_bytes)

    root_clean = root_path.rstrip("/")

    for remote_path, size in files:
        # Ruta relativa respecto a /var/www/html
        rel = remote_path[len(root_clean) + 1 :]  # +1 para saltar la barra
        local_path = os.path.join(local_base, rel)

        local_dir = os.path.dirname(local_path)
        os.makedirs(local_dir, exist_ok=True)

        # Callback por fichero: convertimos (transferred, total) en delta
        last = {"value": 0}

        def callback(transferred, total):
            delta = transferred - last["value"]
            last["value"] = transferred
            progress.add(delta)

        sftp.get(remote_path, local_path, callback=callback)


# -------------------------------------------------
# Programa principal
# -------------------------------------------------

def main():
    config = load_config("config.json")
    root_path = config.get("root_path", "/var/www/html/capitol")

    # Carpeta local YYYYMMDDHHMMSS
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    local_base = os.path.join(os.getcwd(), timestamp)
    os.makedirs(local_base, exist_ok=True)

    print(f"Contents of {root_path} will be downloaded to: {local_base}")

    ssh = None
    sftp = None

    try:
        ssh = create_ssh_client(config)
        sftp = ssh.open_sftp()

        print("Collecting remote file list...")
        files = collect_remote_files(sftp, root_path)
        print(f"Found {len(files)} files. Starting download...")

        download_with_progress(sftp, files, root_path, local_base)

        print("Download finished.")

    finally:
        if sftp is not None:
            sftp.close()
        if ssh is not None:
            ssh.close()


if __name__ == "__main__":
    main()

