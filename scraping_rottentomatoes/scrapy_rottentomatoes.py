from bs4 import BeautifulSoup
import requests as req
import json

#url alvo do scraping.
url_base = "https://www.rottentomatoes.com/browse/tv_series_browse/sort:popular?page=3"

#função responsável por extrair os dados da página web.
def raspar_dados():

    dados = []

    #tratamento de exceções
    try:
        response = req.get(url_base)

        #verifica se a requisição HTTP foi bem-sucedida.
        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")
            series = soup.find_all(["div", "a"], class_="js-tile-link")

            
            for serie in series:
                get = serie.find
                nome = get("span", class_="p--small").text
                critica_score = get("score-pairs")["criticsscore"]
                audiencia_score = get("score-pairs")["audiencescore"]

                nome = nome.replace('\n', '').strip()

                dados.append({"nome":nome, "critica_score":critica_score, "audiencia_score":audiencia_score})

                
        elif response.status_code == 404:
            raise Exception("Página não encontrada!")
            
        else:
            raise Exception(f"requisição falhou, status_code: {response.status_code}")
            

    except Exception as e:
        print(e)
        return []

    else:
        print("pagina varrida com sucesso!")
        return dados

#função responsável por tratar os dados brutos do scraping.
def tratar_dados(dados):

    for dado in dados:

        #remove caracteres "\n" e os espaços antes e após o nome.
        dado["nome"] = dado["nome"].replace('\n', '').strip()
        
        #Trata dados ausentes.
        dado["critica_score"] = (dado["critica_score"] + "%") if (dado["critica_score"] != "") else "N/A" 

        dado["audiencia_score"] = (dado["audiencia_score"] + "%") if (dado["audiencia_score"] != "") else "N/A"

    return dados
        

#função responsável por gravar os dados tratados em um arquivo JSON.
def gravar_dados(dados):
    
    try:
        with open("tv_series.json", "w", newline="", encoding="utf-8") as file:

            json.dump(dados, file, indent=4)

    except Exception as e:
        print("Ocorreu um erro:", e)

    else:
        print("Dados gravados com sucesso!")

#função principal, executa a lógica do script.
def main():
    dados_brutos = raspar_dados()
    
    if dados_brutos:
        dados_tratados = tratar_dados(dados_brutos)
        gravar_dados(dados_tratados)

    else:
        print("O scrapy não retornou dados.")

    print("Fim do scrapy!")


if __name__ == "__main__":
    main()
