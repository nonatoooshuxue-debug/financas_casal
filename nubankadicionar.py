from fastapi import FastAPI
from sqlalchemy import create_engine
import psycopg2 as p
from pydantic import BaseModel
from datetime import date
from decimal import Decimal
import pandas as pd


url_fatura = "postgresql://postgres.uoiwjdeyssumnqvjypcm:jemimalucasnonato@aws-0-sa-east-1.pooler.supabase.com:5432/postgres"
app = FastAPI()
class Gastos(BaseModel):
    Data: date
    Valor: Decimal
    Descrição: str
    Responsavel: str


def meubanco_():
    fatura = p.connect(url_fatura)
    fatura1 = fatura.cursor()
    fatura1.execute("""
    CREATE TABLE IF NOT EXISTS meus_gastos (
    data DATE,
    valor DECIMAL, 
    descricao TEXT NOT NULL,
    responsavel VARCHAR(50)
    )
    """)
    fatura.commit()
    df = pd.read_sql("SELECT * FROM meus_gastos", fatura)
    fatura.close()
    return df

meubanco_()

@app.post("/adicionar-gastos")
def adicionar(gastos: Gastos):
    fatura = p.connect(url_fatura)
    fatura1 = fatura.cursor()
    fatura1.execute(""" 
    INSERT INTO meus_gastos (data, valor, descricao, responsavel) VALUES (%s, %s, %s, %s) """,
    (gastos.Data, gastos.Valor, gastos.Descrição, gastos.Responsavel)
    )
    fatura.commit()
    fatura.close()

    return {"mensagem:" "Gasto adicionado!"}

