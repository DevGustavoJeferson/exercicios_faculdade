#1. IMPORTAMOS AS BIBLIOTECAS NECESSARIAS PARA FAZER OS GRAFICOS(PYPLOYT) E A MINIPULACAO DE DADOS(PANDAS)
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#2. ESTABELECEMOS A CONEXÃO E O NOSSO CURSOR
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
#3. CRIAMOS A TABELA, COM NOSSO CURSOR SQL
cursor.execute("""
CREATE TABLE vendas1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_venda TEXT,
    produto TEXT,
    categoria TEXT,
    valor_venda REAL
)
""")
#4. AQUI INSERI OS DADOS DE UM JEITO MAIS ELABORADO, COM EXECUTEMANY.
inserts = [
 ('2023-01-01','Produto A','Eletrônicos',1500.00),
 ('2023-01-05','Produto B','Roupas',350.00),
 ('2023-02-10','Produto C','Eletrônicos',1200.00),
 ('2023-03-15','Produto D','Livros',200.00),
 ('2023-03-20','Produto E','Eletrônicos',800.00),
 ('2023-04-02','Produto F','Roupas',400.00),
 ('2023-05-05','Produto G','Livros',150.00),
 ('2023-06-10','Produto H','Eletrônicos',1000.00),
 ('2023-07-20','Produto I','Roupas',600.00),
 ('2023-08-25','Produto J','Eletrônicos',700.00),
 ('2023-09-30','Produto K','Livros',300.00),
 ('2023-10-05','Produto L','Roupas',450.00),
 ('2023-11-15','Produto M','Eletrônicos',900.00),
 ('2023-12-20','Produto N','Livros',250.00)
]
cursor.executemany("INSERT INTO vendas1 (data_venda, produto, categoria, valor_venda) VALUES (?,?,?,?)", inserts)
conn.commit()

#5. LEMOS O DATABASE DIRETAMENTE, E CONVERTEMOS EM DATAFRAME USANDO O PANDAS
df = pd.read_sql_query("SELECT * FROM vendas1", conn)
#6. PARA MELHORAR A MANIPULAÇÃO, CONVERTEMOS A COLUNA 'DATA_VENDAS', PARA UM FORMATO DE DATATIME.
df['data_venda'] = pd.to_datetime(df['data_venda'])

#7. AQUI NÓS CONFERIMOS NOSSA DATABASE, EM DATAFRAME
print("Primeiros registros:")
print(df.head(), "\n")

#8. AQUI VAMOS CONFERIR AS INFORMAÇÕES DO NOSSO DATAFRAME
print("Informações do DataFrame:")
print(df.info(), "\n")

#9. O NOSSO 'DESCRIBE' VAI FORNECER VARIAS ESTATISTICAS IMPORTANTES FINANCEIRAMENTE FALANDO
print("Estatísticas descritivas do valor_venda:")
print(df['valor_venda'].describe(), "\n")

#10. INSNULL E SUM, SOMA E MOSTRA QUANTOS VALORES NULOS TEM NA NOSSA TABELA
print("Valores nulos:\n", df.isnull().sum(), "\n")
#11. DUPLICATED, MOSTRA SE EXISTEM VALORES DUPLICADOS E SUBSET MOSTRA AS COLUNAS QUE IRÃO PASSAR PELO DUPLICATED, E NO FIM SOMA
print("Duplicados:", df.duplicated(subset=['data_venda','produto','categoria','valor_venda']).sum(), "\n")

#12. AQUI NOS CRIAMOS COLUNAS EM CIMA DE 'DATA_VENDA', E CONVERTEMOS SEU FORMATO, PARA FAZER ANALISE DE DADOS COM GRAFICOS
df['ano'] = df['data_venda'].dt.year
df['mes'] = df['data_venda'].dt.month
df['mes_ano'] = df['data_venda'].dt.to_period('M').astype(str)

#13. 'GROUPBY' VAMOS AGRUPAR TUDO OQUE ESTIVER NA COLUNA 'CATEGORIA'(TABELA UNIDIMENSIONAL)
#13.1 VAMOS SOMAR TUDO QUE ESTIVER EM 'VALOR_VENDAS' E ESSAS DUAS COLUNAS IRÃO SE AGRUPAR
#13.2 'SORT_VALUES' DETERMINA QUE A ORGANIZAÇÃO DA TABELA SERÁ DO MAIOR PARA O MENOR
#13.3 O RESULTADO É UMA TABELA QUE IRÁ SOMAR OS VALORES TOTAIS POR CATEGORIA EM ORDEM CRESCENTE
total_por_categoria = df.groupby('categoria')['valor_venda'].sum().sort_values(ascending=False)
#14. FAZEMOS O MESMO QUE O PASSO "13" SÓ QUE AGORA COM OS PRODUTOS
total_por_produto = df.groupby('produto')['valor_venda'].sum().sort_values(ascending=False)

#15. RESAMPLE FUNCIONA QUANDO O ÍNDICE DO DATAFRAME É UM "DATATIME", OU SEJA ELE SE CONECTA COM O PASSO 6
#15.1 RESAMPLE VAI SEPARAR AS VENDAS POR PERIODO(NESSE CASO O 'M'(MES)), E DEPOIS SOMAR NUMA TABELA
vendas_mensais = df.set_index('data_venda')['valor_venda'].resample('M').sum()

#16 AQUI CONSEGUIMOS VER NOSSOS INSIGHTS, QUE CRIAMOS NOS PASSOS 13,14 E 15
print("Total por categoria:\n", total_por_categoria, "\n")
print("Top produtos:\n", total_por_produto.head(), "\n")
print("Vendas mensais:\n", vendas_mensais, "\n")


#17 VAMOS AGORA EXIBIR NOSSOS RESULTADOS COM PYPLOT + PANDAS, MAIS RAPIDO E CLEAN
total_por_categoria.plot(kind='bar', figsize=(6,4), title="Total de vendas por categoria")
plt.ylabel("Valor total (R$)")
plt.show()
total_por_produto.head(10).plot(kind='bar', figsize=(8,4), title="Top 10 produtos por receita")
plt.ylabel("Valor total (R$)")
plt.show()
vendas_mensais.plot(marker='o', figsize=(8,4), title="Vendas mensais")
plt.ylabel("Valor total (R$)")
plt.show()

#18 PARA MELHOR VISUALIZAÇÃO VAMOS COLOCAR UM HISTOGRAMA
df['valor_venda'].plot(kind='hist', bins=8, figsize=(6,4), title="Distribuição dos valores de venda")
plt.xlabel("Valor da venda (R$)")
plt.show()

#19 QUIS FAZER UM BOXPLOT POR CATEGORIA UTILIZANDO O SEABORN PARA DEIXAR O CODIGO MAIS CLEAN
plt.figure(figsize=(6,4))
sns.boxplot(x="categoria", y="valor_venda", data=df, palette="Set2")
plt.title("Boxplot - valores por categoria")
plt.ylabel("Valor da venda (R$)")
plt.xlabel("Categoria")
plt.show()

#20 VAMOS CRIAR UM RESUMO COM O PANDAS
resumo = pd.DataFrame({
    'Total (R$)': total_por_categoria,
    'Média (R$)': df.groupby('categoria')['valor_venda'].mean(),
    'Quantidade': df['categoria'].value_counts()
})
print("\nResumo por categoria:\n", resumo, "\n")

#21 VAMOS DAR A EMPRESA CONCLUSÕES DOS DADOS
print("===== Conclusões Automáticas =====")
categoria_top = total_por_categoria.idxmax()
valor_top = total_por_categoria.max()
print(f"A categoria com maior receita foi **{categoria_top}**, com um total de R${valor_top:.2f}.")

produto_top = total_por_produto.idxmax()
valor_produto_top = total_por_produto.max()
print(f"O produto com maior receita foi **{produto_top}**, com R${valor_produto_top:.2f}.")

mes_top = vendas_mensais.idxmax().strftime("%B/%Y")
valor_mes_top = vendas_mensais.max()
print(f"O mês com maior faturamento foi **{mes_top}**, totalizando R${valor_mes_top:.2f}.")

#22 POR FIM VAMOS DAR SUGESTÕES COM BASE NOS DADOS EXIBIDOS E ANALISADOS
print("Sugestões:")
print("- Manter foco em Eletrônicos, já que concentram maior parte da receita.")
print("- Avaliar promoções em meses de baixo desempenho.")
print("- Produtos com receita baixa podem ser analisados para ajuste de preço, marketing ou retirada do catálogo.")
