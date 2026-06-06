#!/usr/bin/env python3
# ============================================================
# RESTORE ODYSSEUS FROM GITHUB
# ============================================================
# Downloads and restores Odysseus from sunken-sh1p repo
# ============================================================

import os
import subprocess
import requests
import tarfile
import zipfile
from pathlib import Path
import shutil

print("=" * 80)
print("💜 RESTORE ODYSSEUS FROM GITHUB")
print("=" * 80)

REPO_OWNER = "kimochione"
REPO_NAME = "sunken-sh1p"
BRANCH = "main"
INSTALL_DIR = Path("/content/odysseus_restored")

def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(dest_path, 'wb') as f:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                print(f"\r   Progress: {percent:.1f}%", end="", flush=True)
    print()
    return dest_path.exists()

def download_directory(api_path, local_dir):
    api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{api_path}"
    response = requests.get(api_url)
    if response.status_code != 200:
        return 0
    count = 0
    for item in response.json():
        if item['type'] == 'file':
            local_path = local_dir / item['name']
            local_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"   Downloading {item['name']}...")
            download_file(item['download_url'], local_path)
            os.chmod(local_path, 0o755)
            count += 1
        elif item['type'] == 'dir':
            subdir = local_dir / item['name']
            subdir.mkdir(parents=True, exist_ok=True)
            count += download_directory(f"{api_path}/{item['name']}", subdir)
    return count

INSTALL_DIR.mkdir(parents=True, exist_ok=True)

print("\n📥 Downloading Odysseus files...")
total = download_directory("odysseus_backup", INSTALL_DIR)
print(f"\n✅ Downloaded {total} files")

print("\n🔧 Installing dependencies...")
subprocess.run(["pip", "install", "-r", str(INSTALL_DIR / "requirements.txt")], capture_output=False)

print("\n🚀 Starting Odysseus...")
subprocess.run(["python", str(INSTALL_DIR / "app.py")], capture_output=False)

print("\n" + "=" * 80)
print("💜 Restore complete! Ara ara~")
print("=" * 80)
