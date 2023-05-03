import pandas as pd
from config import mssq_datawharehouse
from sqlalchemy import text
from apyori import apriori
from itertools import chain
import json
from collections import OrderedDict


def pedidos_itens() -> None:
        
    enginemssql = mssq_datawharehouse()
    with enginemssql.begin() as conn:
        get_items = conn.execute(text("""
        SELECT DISTINCT pedidos.ref_venda,pedidos.ref_produto, pedidos.quantidade   
        ,pedidos.[data_cadastro],produtos.nome_produto,pedidos.bit_showroom,produtos.marca,pedidos.ref_contrato
        FROM datawharehouse.comercial.dim_pedido as pedidos
        left join comercial.dim_produtos as produtos on produtos.ref_produto = pedidos.ref_produto
        where pedidos.ref_venda is not null and year(pedidos.data_cadastro) >= '2022'""")).all()
        
        dict_tems = [row._asdict() for row in get_items]
        yield dict_tems


def get_dataframe() -> pd.DataFrame:
    data = pedidos_itens()
    dicts = [args for args in chain.from_iterable(data)]
    
    pedidos_df = pd.DataFrame(dicts)
    pedidos_df = pedidos_df.dropna()
    pedidos_df = pedidos_df.drop_duplicates()
    pedidos_df.sort_values(by=['data_cadastro','quantidade'],ascending=False)
    new_list_pedidos = pedidos_df[['ref_contrato', 'ref_produto', 'quantidade', 'data_cadastro','marca']]
   
    return new_list_pedidos


def apriori_df() -> list:
    new_list_pedidos = get_dataframe()
    cont = len(new_list_pedidos)
    cools = len(new_list_pedidos.columns)
    transacoes = []
    for i in range(0, cont):
        transacoes.append([str(new_list_pedidos.values[i, j]) for j in range(0, cools)])
    return transacoes


def calculate_apriori() -> None:
    lista_apriori = []
    transacoes = apriori_df()
    new_transacoes= [item for item in transacoes]
    regras = apriori(new_transacoes, min_support=0.003,
                      min_confidence=0.01, min_lift=0.01, min_lenght=2)

    resultados = list(regras)
    cont = len(resultados)
    i = 1
    while i < cont:
        if resultados[i] !=None:
            lista_apriori.append(resultados[i])

        i +=1
    print(lista_apriori)
calculate_apriori()