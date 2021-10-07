
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

navegador = webdriver.Chrome("/usr/local/bin/chromedriver")

# Passo 1: Pegar a cotação do Dólar
# entrar no site do google
navegador.get("https://www.google.com/")
# pesquisar "cotação dólar"
navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação dólar")
navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
# pegar a cotação da página do google
cotacao_dolar = navegador.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
print(cotacao_dolar)

# Passo 2: Pegar a cotação do Euro
navegador.get("https://www.google.com/")
#pesquisar cotaçao euro
navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação euro")
navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
cotacao_euro = navegador.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
print(cotacao_euro)

# Passo 3: Pegar a cotação do Ouro
navegador.get("https://www.melhorcambio.com/ouro-hoje")
cotacao_ouro = navegador.find_element_by_xpath('//*[@id="comercial"]').get_attribute("value")
cotacao_ouro = cotacao_ouro.replace(",",".")
print(cotacao_ouro)



# Passo 4: Importar a base de dados
tabela = pd.read_excel("Produtos.xlsx")
print(tabela)

# Passo 5: Atualizar a cotação, o preço de compra e o preço de venda
# atualizar cotaçao
print(cotacao_dolar)
tabela.loc[tabela["Moeda"] == "Dólar", "Cotação"] = float(cotacao_dolar)
tabela.loc[tabela["Moeda"] == "Euro", "Cotação"] = float(cotacao_euro)
tabela.loc[tabela["Moeda"] == "Ouro", "Cotação"] = float(cotacao_ouro)

# atualizar preço de comprar = preço original*cotaçao
tabela["Preço Base Reais"] = tabela["Preço Base Original"] * tabela["Cotação"]

# atualizar o preço de venda = preço de compra *margem
tabela["Preço Final"] = tabela["Preço Base Reais"] * tabela["Margem"]

print(tabela)
# Passo 6: Exportar o relatório atualizado

tabela.to_excel("Produto_novo.xlsx", index=False)
navegador.quit()