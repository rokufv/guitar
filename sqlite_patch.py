import sys
import sqlite3
import platform

def patch_sqlite():
    if platform.system() != "Linux":
        return
        
    try:
        import pysqlite3
        sys.modules["sqlite3"] = pysqlite3
    except ImportError:
        pass

if __name__ == "__main__":
    patch_sqlite()
    print(f"Current SQLite version: {sqlite3.sqlite_version}") 