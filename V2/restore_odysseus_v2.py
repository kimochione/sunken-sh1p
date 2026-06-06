#!/usr/bin/env python3
# ============================================================
# RESTORE ODYSSEUS V2 FROM GITHUB (ZIP VERSION)
# ============================================================
# Downloads 10 ZIP files from sunken-sh1p/V2/
# Unzips and restores Odysseus
# ============================================================

import os
import zipfile
import requests
from pathlib import Path
import shutil

print("=" * 80)
print("💜 RESTORE ODYSSEUS V2 FROM GITHUB (ZIP VERSION)")
print("=" * 80)

REPO_OWNER = "kimochione"
REPO_NAME = "sunken-sh1p"
BRANCH = "main"
REMOTE_FOLDER = "V2"
NUM_ZIPS = 10
ZIP_PREFIX = "odysseus_part"

INSTALL_DIR = Path("/content/odysseus_restored_v2")
DOWNLOAD_DIR = Path("/content/odysseus_zips_download")

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

INSTALL_DIR.mkdir(parents=True, exist_ok=True)
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

print("\n📥 Downloading ZIP files from GitHub...")

zip_paths = []
for i in range(NUM_ZIPS):
    zip_name = f"{ZIP_PREFIX}_10.zip"
    zip_path = DOWNLOAD_DIR / zip_name
    download_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{REMOTE_FOLDER}/{zip_name}"
    
    print(f"   Downloading {zip_name}...")
    try:
        download_file(download_url, zip_path)
        if zip_path.exists():
            zip_paths.append(zip_path)
            print(f"      ✅ Downloaded ({zip_path.stat().st_size / (1024*1024):.2f} MB)")
    except Exception as e:
        print(f"      ❌ Failed: {e}")

print(f"\n✅ Downloaded {len(zip_paths)} ZIP files")

print("\n📦 Extracting ZIP files...")
for zip_path in zip_paths:
    print(f"   Extracting {zip_path.name}...")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(INSTALL_DIR)
print("   ✅ Extraction complete")

print("\n🔧 Installing dependencies...")
os.chdir(INSTALL_DIR)
if (INSTALL_DIR / "requirements.txt").exists():
    import subprocess
    subprocess.run(["pip", "install", "-r", "requirements.txt"], capture_output=False)

print("\n🚀 Starting Odysseus...")
subprocess.run(["python", "app.py"], capture_output=False)

print("\n" + "=" * 80)
print("💜 V2 Restore complete! Ara ara~")
print("=" * 80)
