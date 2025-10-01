import os
from fastapi import FastAPI, Header, HTTPException, Path
from fastapi.responses import JSONResponse
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_TOKEN = os.environ.get("API_TOKEN")

def get_db_connection(database: str):
    try:
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            database=database
        )
        return conn
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar ao banco: {e}")

@app.get("/{database}/unidades")
def get_unidades(
    database: str = Path(..., description="Nome da database"),
    token: str = Header(None)
):
    # Verifica token
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")

    conn = get_db_connection(database)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT DISTINCT nome FROM {database}.unidade")
        result = [row[0] for row in cursor.fetchall()]
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Erro na query: {e}")
    finally:
        cursor.close()
        conn.close()

    return JSONResponse(content=result)
