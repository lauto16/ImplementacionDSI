import os
import shutil

DB_FILE = "db.sqlite3"
BKP_FILE = "bkp.sqlite3"
TEMP_FILE = "temp_db.sqlite3"

if not os.path.exists(BKP_FILE):
    print(f"No se encontró {BKP_FILE}. Abortando.")
    exit(1)

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"Archivo {DB_FILE} eliminado.")

shutil.copy(BKP_FILE, TEMP_FILE)
os.rename(TEMP_FILE, DB_FILE)
print(f"Se creó una nueva {DB_FILE} a partir de {BKP_FILE}.")