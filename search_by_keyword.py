import requests
import pandas as pd
from about import greetings
from bs4 import BeautifulSoup
from datetime import datetime

class DETIKScraper:
    greetings()
    def __init__(self, keywords, pages):
        self.keywords = keywords
        self.pages = pages

    def fetch(self, base_url):
        self.base_url = base_url

        self.params = {
            'query': self.keywords,
            'sortby': 'time',
            'page': 2
        }

        self.headers = {
            'sec-ch-ua': '"(Not(A:Brand";v="8", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-platform': "Linux",
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.35 Safari/537.36'
        }

        self.response = requests.get(self.base_url, params=self.params, headers=self.headers)

        return self.response

    def get_articles(self, response):
        article_lists = []

        for page in range(1, int(self.pages)+1):
            url = f"{self.base_url}?query={self.keywords}&sortby=time&page={page}"

            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")

            articles = soup.find_all("article")

            for article in articles:
                title = article.find("h2", {"class": "title"}).get_text()
                category = article.find("span", {"class": "category"}).get_text()
                published_time = article.find("span", {"class": "date"}).get_text().split(",")[1]
                href = article.find("a")["href"]
                article_lists.append({
                    "title": title, 
                    "cateogory": category, 
                    "published_time": published_time, 
                    "href": href})

        self.articles = article_lists

        try:
            self.show_results()
        except Exception as e:
            print(e)
        finally:
            print()
            print( "[~] Scraping finished!")
            print(f"[~] Total Articles: {len(self.articles)}")

        return self.articles

    def save_to(self, file_format="csv"):
        '''  '''
        time_scrape = datetime.now().strftime("%m%d%Y_%H%M%S")

        df = pd.DataFrame(self.articles)

        file_name = f"result_{self.keywords}_{time_scrape}"
        if file_format == "csv":
            file_name += ".csv"
            df.to_csv(file_name, index=False)
            print(f"[~] Result saved to '{file_name}'")
        elif file_format == "excel":
            file_name += ".xlsx"
            df.to_excel(file_name, index=False)
            print(f"[~] Result saved to '{file_name}'")

    def show_results(self, row = 5):
        df = pd.DataFrame(self.articles)
        df.index += 1
        if row:
            print(df.head())
        else:
            print(df)

if __name__ == '__main__':
    keywords = input("[~] Keywords     : ")
    pages =    input("[~] Total Pages  : ")
    base_url = f"https://www.detik.com/search/searchall"

    scrape = DETIKScraper(keywords, pages)
    response = scrape.fetch(base_url)
    articles = scrape.get_articles(response)

    try:
        ask =             input("[~] Do you want save the results? [y/n]: ").lower()
        if ask == 'y':
            file_format = input("[~] File format? [csv/excel]           : ").lower()
            scrape.save_to(file_format=file_format)
        elif ask == 'n':
            scrape.show_results()
    except Exception as e:
        print(e)
    finally:
        print("[~] Program Finished")
