from bs4 import BeautifulSoup
import requests as req
import csv

def raspar_gravar(url, writer):
  #indica a página que está sendo raspada.
  pagina = (int(url.split('=')[1]) // 50) + 1

  print(f"Raspando pagina -> {pagina}")
  response = req.get(url)

  dados = []
  
  #testando a resposta da requisição -> Código 200 == OK
  if response.status_code == 200:

    soup = BeautifulSoup(response.text, "html.parser")
    animes = soup.find_all("tr", class_="ranking-list")

    for anime in animes:

      rank = anime.find("td", class_="rank ac").find("span").text
      nome = anime.find("td", class_="title al va-t word-break").find("h3", class_="fl-l fs14 fw-b anime_ranking_h3").text
      score = anime.find("td", class_="score ac fs14").find("div", class_="js-top-ranking-score-col di-ib al").text

      dados.append([rank, nome, score])

    writer.writerows(dados)

    return True

  else:
    print(f"Requisição à url = {url} falhou!")

    return False

def main():
    
    base_url = "https://myanimelist.net/topanime.php?limit="

    with open("top_animes.csv", "w", newline="", encoding="utf-8") as file:
      writer = csv.writer(file)

      writer.writerow(["Rank", "Nome", "Score"])

      limit_url = 0
      flag = True

      #laço que percore as 3 primeiras páginas do ranking.
      while flag and limit_url <= 100:
        url = base_url + str(limit_url)
        flag = raspar_gravar(url, writer)
        limit_url += 50

    print("Scrapy concluído!")

if __name__ == "__main__":
    main()
