# hashguard
File integrity check tool.  It retrieves and saves the SHA-256 hashes of files in a folder, and then checks for any changes.


# hashguard 🔐

A simple file integrity monitoring tool.

## Features
- SHA-256 hashing
- Detects modified, deleted, and new files
- No dependencies
- Cross-platform

## Usage
check your changes: python3 hashguard.py check /path/to/folder

Initialize hash database:
```bash
python3 hashguard.py init /path/to/folder

