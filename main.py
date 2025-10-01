import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import mysql.connector
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

app = FastAPI()

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        database=os.environ.get("DB_NAME")
    )

@app.get("/unidades")
def get_unidades():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT nome FROM qualyteam_testevinicius.git initunidade")
    result = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return JSONResponse(content=result)
