import streamlit as st
import requests
import pandas as pd
from nubankadicionar import meubanco_

st.set_page_config(layout="wide")
url_projeto = "http://127.0.0.1:8000/adicionar-gastos"

try:
    with st.sidebar:
     st.header("MEU MINI SISTEMA ERP - GASTOS")
     with st.form("Gastos:"):
        data = st.date_input("Data")
        valor = st.number_input("Valor", min_value=0.0, format="%.2f")
        Descrição = st.text_input("Descrição")
        Responsavel = st.text_input("Responsavel")
        enviar = st.form_submit_button("Adicionar o Gasto")
        if enviar:
            dadoszin = { 
                "Data": str(data),
                "Valor": valor,
                "Descrição": Descrição,
                "Responsavel": Responsavel
            }
            requestezin = requests.post(url_projeto, json=dadoszin)
            if requestezin.status_code in [200, 201]:
                st.success("Gasto adicionado com sucesso, paizão!")
            else: 
                st.error(f"Erro: {requestezin.text}")
except Exception as e:
    print("Deu ruim, rapaziada!")

st.header("TABELA DOS MEUS GASTOS:")
df_ = meubanco_()
faturas_div = df_.groupby("responsavel")["valor"].sum()
meus = faturas_div.get("LUCAS", 0.0)
jemima = faturas_div.get("JEMIMA", 0.0)
r = st.columns(2)
r[0].metric(label="GASTOS - LUCAS:", value=f"{meus: ,.2f}")
r[1].metric(label="GASTOS - JEMIMA:", value=f"{jemima: ,.2f}")


st.dataframe(df_, hide_index=True, use_container_width=True)





