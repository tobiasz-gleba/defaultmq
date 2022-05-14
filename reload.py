import hashlib
from pathlib import Path
import os
from time import sleep


def md5_update_from_file(filename, hash):
    assert Path(filename).is_file()
    with open(str(filename), "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash


def md5_file(filename):
    return md5_update_from_file(filename, hashlib.md5()).hexdigest()


def md5_update_from_dir(directory, hash):
    assert Path(directory).is_dir()
    for path in sorted(Path(directory).iterdir()):
        hash.update(path.name.encode())
        if path.is_file():
            hash = md5_update_from_file(path, hash)
        elif path.is_dir():
            hash = md5_update_from_dir(path, hash)
    return hash


def md5_dir(directory):
    return md5_update_from_dir(directory, hashlib.md5()).hexdigest()

old_md5_hash = ""
while True:
    sleep(0.3)
    md5_hash =  md5_dir("src")
    if old_md5_hash != md5_hash:
        # print(old_md5_hash)
        print("\n\n\n\n !new verson! \n\n\n\n")
        os.system("docker-compose up -d --build --remove-orphans && docker-compose up -d --build --no-deps defaultmq && docker logs defaultmq")
        old_md5_hash = md5_hash



