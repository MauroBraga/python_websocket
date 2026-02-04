# EXECUTAR REQUIREMTNS.TXT
# pip install -r requirements.txt

#Criado Banco de Dados
flask shell

db.create_all()
exit()



>>> db.drop_all()
>>> db.create_all()


---
Environment troubleshooting

1) ModuleNotFoundError: No module named '_sqlite3'

   This project uses SQLAlchemy and on some Linux/macOS Python builds the
   C-backed `_sqlite3` extension isn't available which causes `import sqlite3`
   to fail. Two options to fix:

   A) System-level (recommended): install the SQLite development packages
      and rebuild or reinstall your Python. On Debian/Ubuntu:

      sudo apt update && sudo apt install -y libsqlite3-dev sqlite3

      Then reinstall Python or use your system Python.

   B) Quick Python fallback (works without rebuilding Python): install the
      pysqlite3 shim in your virtualenv:

      pip install pysqlite3-binary

      The application already attempts to import `pysqlite3` if `sqlite3`
      is missing.

2) SocketIO and running the app

   Requirements include `Flask-SocketIO`. Install deps and run the app:

       pip install -r requirements.txt
       python app.py

3) Validation checklist

   - pip install -r requirements.txt
   - (optional) pip install pysqlite3-binary if you cannot install system sqlite
   - Run `python app.py` and verify the server starts without ImportError
   - POST to /payments/pix with JSON {"value": 10} to create a payment

---
