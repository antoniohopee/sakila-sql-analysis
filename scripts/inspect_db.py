from pathlib import Path
import sqlite3


ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "data" / "sakila.db"


def inspect_database() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database non trovato: {DB_PATH}. "
            "Esegui prima: python scripts/download_db.py"
        )

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name;
        """)

        tables = cursor.fetchall()

    print("Tabelle trovate nel database:")
    for table in tables:
        print(f"- {table[0]}")


if __name__ == "__main__":
    inspect_database()