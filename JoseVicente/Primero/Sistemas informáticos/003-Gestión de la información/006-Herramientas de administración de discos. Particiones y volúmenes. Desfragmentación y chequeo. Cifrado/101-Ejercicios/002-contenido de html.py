import json
import stat
import paramiko

def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    cfg = load_config("config.json")

    host = cfg["host"]
    port = cfg.get("port", 22)
    user = cfg["username"]
    password = cfg["password"]
    remote_path = cfg.get("path", "/var/www/html")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=port, username=user, password=password)

    sftp = ssh.open_sftp()

    try:
        print(f"Contents of {remote_path}:\n")

        for entry in sftp.listdir_attr(remote_path):
            name = entry.filename
            mode = entry.st_mode

            if stat.S_ISDIR(mode):
                print(f"[DIR ] {name}")
            else:
                print(f"[FILE] {name}")

    finally:
        sftp.close()
        ssh.close()

if __name__ == "__main__":
    main()

