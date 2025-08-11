import os, pathlib, pyodbc
server = os.environ['AZURE_SQL_SERVER']
db     = os.environ['AZURE_SQL_DB']
user   = os.environ['AZURE_SQL_USER']
pwd    = os.environ['AZURE_SQL_PASSWORD']
driver = os.environ.get('AZURE_SQL_DRIVER','ODBC Driver 18 for SQL Server')
conn = pyodbc.connect(f"DRIVER={{{driver}}};SERVER={server};DATABASE={db};UID={user};PWD={pwd};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
cur = conn.cursor()
cur.execute("IF OBJECT_ID('dbo.positions','U') IS NOT NULL DROP TABLE dbo.positions;")
conn.commit()
sql_path = pathlib.Path(__file__).parent / 'positions.sql'
cur.execute(open(sql_path, encoding='utf-8').read())
conn.commit()
print('Seeded positions.')
conn.close()