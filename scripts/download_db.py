from pathlib import Path
import requests


DB_URL = "https://raw.githubusercontent.com/bradleygrant/sakila-sqlite3/main/sakila_master.db"

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "sakila.db"


def download_database() -> None:
    DATA_DIR.mkdir(exist_ok=True)

    if DB_PATH.exists():
        print(f"Database già presente: {DB_PATH}")
        return

    print("Download del database Sakila in corso...")

    response = requests.get(DB_URL, timeout=30)
    response.raise_for_status()

    DB_PATH.write_bytes(response.content)

    print(f"Database scaricato correttamente in: {DB_PATH}")


if __name__ == "__main__":
    download_database()