
# Dashboards Tableau

# marketbasket
# Fazer JOIN da tabela Pedidos vs Ela mesma para confrontar os valores de uma com a outra

# lif
# COUNTD([Co-occurance Order IDs])*COUNTD([ID do pedido])/(COUNTD([Antecedent All Order IDs])*COUNTD([Consequent All Order IDs]))

# Suporte

# COUNTD([Antecedent All Order IDs])/COUNTD([ID do pedido])

# Confidence

# COUNTD([Co-occurance Order IDs])/COUNTD([Antecedent All Order IDs])

# Parametros
# Sub Categoria1
# Sub Categoria2



# Cohort Tempo Recompra |Churn


# Campo Calculado "Primeira Compra"
# {FIXED [Customer Name]:MIN([Order Date])}

# Campo calculado "Segunda Compra"
# {FIXED [Customer Name]: MIN(
# IF [Order Date] > [Primeira Compra do Cliente] THEN
# [Order Date]
# END
# )}


# Tempo para Recompra
# DATEDIFF('quarter', [Primeira Compra do Cliente],[Segunda Compra])




# Apriory Python

##Execução do projeto
<br>criar venv: py -3 -m venv venv<br/>
<br>ativar: venv\Scripts\activate<br/>
<br>instalar dependencias: pip freeze > requirements.txt<br/>



```Python

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
        ...

<br>A função sqlachemy responsavel por executar a consulta da tabela de produtos e retornar para a função do Apriori. Checar se nao esta vindo arquilvos NULL <br/>

``` Python
def mssql_get_conn():

    connection_url = URL.create(
            "mssql+pyodbc",
            username=f"{myboxuser_mssql}",
            password=f"{myboxpassword_mssql}",
            host=f"{myboxhost_mssql}",
            database=f"{myboxdatabase_mssql}",
            query={
                "driver": "ODBC Driver 17 for SQL Server",
                "autocommit": "True",
        },
        )
      
    engine = create_engine(connection_url).execution_options(
    isolation_level="AUTOCOMMIT", future=True,fast_executemany=True)
    return engine

```

<br>Função engine responsavel por fazer conexao com o banco de dados SQL Server "Nao esquecer de criar o arquivo .env e informar as credenciais."<br/>



``` Python
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

```

<br>Função principal, responsavel por fazer a chamada de todas as demais, iterar no Fronzenset e salva-lo em uma lista."Sempre checar se os valores min_support,min_confidence,min_lift e min_lenght"  estão de acordo com a configuração, pode variar dependendo do tamanho da relação de pedidos<br/>