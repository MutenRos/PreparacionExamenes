import json
import os
import stat
import paramiko


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
        passphrase = auth.get("passphrase")  # may be None
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


def is_dir(sftp, path: str) -> bool:
    """
    Return True if 'path' is a directory on the remote system.
    """
    try:
        attr = sftp.stat(path)
    except IOError:
        return False
    return stat.S_ISDIR(attr.st_mode)


def walk_remote(sftp, root_path: str, prefix: str = "", depth: int = 0, max_depth: int | None = None):
    """
    Recursively list remote directory tree, similar to 'tree' command.

    prefix   : ASCII tree prefix accumulated (e.g. '│   ')
    depth    : current depth (root = 0)
    max_depth: limit depth; None = no limit
    """
    if max_depth is not None and depth > max_depth:
        return

    try:
        entries = sftp.listdir_attr(root_path)
    except IOError as e:
        print(f"{prefix}[ERROR opening {root_path}: {e}]")
        return

    # Sort entries alpha (dirs first, then files)
    entries_sorted = sorted(
        entries,
        key=lambda e: (not stat.S_ISDIR(e.st_mode), e.filename.lower())
    )

    count = len(entries_sorted)
    for idx, entry in enumerate(entries_sorted):
        name = entry.filename
        remote_path = os.path.join(root_path, name)

        is_directory = stat.S_ISDIR(entry.st_mode)
        is_last = (idx == count - 1)

        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{name}{'/' if is_directory else ''}")

        if is_directory:
            # Compute new prefix for children
            child_prefix = prefix + ("    " if is_last else "│   ")
            walk_remote(
                sftp,
                remote_path,
                prefix=child_prefix,
                depth=depth + 1,
                max_depth=max_depth,
            )


def main():
    config = load_config("config.json")

    root_path = config.get("root_path", ".")
    max_depth = config.get("max_depth")  # can be None

    ssh = None
    sftp = None

    try:
        ssh = create_ssh_client(config)
        sftp = ssh.open_sftp()

        # Print root
        print(root_path.rstrip("/") + "/")
        walk_remote(sftp, root_path, prefix="", depth=0, max_depth=max_depth)

    finally:
        if sftp is not None:
            sftp.close()
        if ssh is not None:
            ssh.close()


if __name__ == "__main__":
    main()

