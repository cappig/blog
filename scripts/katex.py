import requests
import zipfile
import shutil
from pathlib import Path

STATIC_DIR = Path("static")
KATEX_DIR = STATIC_DIR / "katex"
VERSION_FILE = KATEX_DIR / "version.txt"
GITHUB_API = "https://api.github.com/repos/KaTeX/KaTeX/releases/latest"


def get_latest_version():
    print("Fetching latest katex release... ", end="", flush=True)

    response = requests.get(GITHUB_API)
    response.raise_for_status()
    data = response.json()

    version = data["tag_name"].lstrip("v")
    download_url = None

    for asset in data["assets"]:
        if asset["name"] == f"katex.zip":
            download_url = asset["browser_download_url"]
            break

    print("done")

    return version, download_url


def download_katex(url, version):
    print(f"Downloading katex v{version}...", end="", flush=True)

    response = requests.get(url, stream=True)
    response.raise_for_status()

    zip_path = STATIC_DIR / "katex.zip"

    with open(zip_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print("done")

    return zip_path


def extract_katex(zip_path):
    print("Extracting files... ", end="", flush=True)

    if KATEX_DIR.exists():
        shutil.rmtree(KATEX_DIR)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(STATIC_DIR)

    zip_path.unlink()

    print("done")


def save_version(version):
    with open(VERSION_FILE, "w") as f:
        f.write(version)


def main():
    STATIC_DIR.mkdir(exist_ok=True)

    version, download_url = get_latest_version()
    zip_path = download_katex(download_url, version)

    extract_katex(zip_path)
    save_version(version)

if __name__ == "__main__":
    main()
