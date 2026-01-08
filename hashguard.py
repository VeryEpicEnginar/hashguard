#!/usr/bin/env python3

import hashlib
import json
import os
import sys

HASH_FILE = ".hashguard.json"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def scan(directory):
    data = {}
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            if file == HASH_FILE:
                continue
            try:
                data[full_path] = sha256(full_path)
            except Exception:
                pass
    return data


def save(data):
    with open(HASH_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load():
    if not os.path.exists(HASH_FILE):
        print("[-] Hash file not found. Run init first.")
        sys.exit(1)
    with open(HASH_FILE, "r") as f:
        return json.load(f)


def init(directory):
    print("[*] Initializing hash database...")
    data = scan(directory)
    save(data)
    print("[+] Hash database created.")


def check(directory):
    print("[*] Checking integrity...")
    old = load()
    new = scan(directory)

    modified = []
    for file, old_hash in old.items():
        if file not in new:
            modified.append(f"[DELETED] {file}")
        elif new[file] != old_hash:
            modified.append(f"[MODIFIED] {file}")

    for file in new:
        if file not in old:
            modified.append(f"[NEW] {file}")

    if not modified:
        print("[+] No changes detected.")
    else:
        print("⚠ Changes detected:")
        for m in modified:
            print(m)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: hashguard.py <init|check> <directory>")
        sys.exit(1)

    command = sys.argv[1]
    directory = sys.argv[2]

    if command == "init":
        init(directory)
    elif command == "check":
        check(directory)
    else:
        print("Unknown command.")
