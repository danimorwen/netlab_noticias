import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from elasticsearch import Elasticsearch

# this class collects news' urls from G1 Portal using the following filters: query: "desinformação", species: "notícias"
class NewsUrlsCollector:
    def collect(self, max_page):
        news_urls = []
        for number in range(1, max_page + 1):
            news_urls.extend(self.__get_page_links(number))
        return news_urls

    def __get_page_links(self, page_number):
        url = f"https://g1.globo.com/busca/?q=desinforma%C3%A7%C3%A3o&order=recent&species=not%C3%ADcias&page={page_number}"
        response = requests.get(url).content
        soup = BeautifulSoup(response, "html.parser")
        text_containers = soup.find_all(class_="widget--info__text-container")
        page_urls = []
        for container in text_containers:
            page_urls.extend(self.__extract_news_link(container))
        return page_urls

    def __extract_news_link(self, container):
        raw_url = container.find("a")["href"]
        parsed_url = urlparse(raw_url)
        return parse_qs(parsed_url.query)["u"]


# this class extracts title, date and content information from the previously collected articles
class NewsContentExtractor:
    def extract(self, url):
        article_dict = {}
        response = requests.get(url).content
        soup = BeautifulSoup(response, "html.parser")
        article_dict["titulo"] = self.__get_title(soup)
        article_dict["data"] = self.__get_date(soup)
        article_dict["corpo"] = self.__get_body(soup)
        return article_dict

    def __get_title(self, soup):
        raw_title = soup.select("h1.content-head__title")
        if len(raw_title) > 0:
            return raw_title[0].text
        return ""

    def __get_date(self, soup):
        raw_date = soup.find("time")["datetime"]
        if raw_date is not None:
            return raw_date
        return ""

    def __get_body(self, soup):
        body_list = []
        body_css = soup.select("div.mc-column.content-text.active-extra-styles")
        for body in body_css:
            news_text = body.text
            body_list.append(news_text.strip())
        return " ".join(body_list)


# this class uses NewsUrlsCollector and NewsContentExtractor to fetch and parse news information
class DisinformationNewsCollector:
    def __init__(self):
        self.news_urls_collector = NewsUrlsCollector()
        self.news_extractor = NewsContentExtractor()

    def collect(self):
        news_urls = self.news_urls_collector.collect(4)
        return self.__fetch_news_content(news_urls)

    def __fetch_news_content(self, url_list):
        news_list = []
        for url in url_list:
            news_list.append(self.news_extractor.extract(url))
        return news_list


# this class is an abstration layer to interface with ElasticSearch
class ElasticsearchClient:
    def __init__(self):
        self.es = Elasticsearch(["http://elasticsearch:9200"])
        print("Connected to Elasticsearch")

    def create_index(self, index, mapping):
        if not self.es.indices.exists(index=index):
            self.es.indices.create(index=index, mappings=mapping)

    def add_documents(self, documents, index):
        for document in documents:
            self.es.create(index=index, document=document)


news_collector = DisinformationNewsCollector()
disinformation_news = news_collector.collect()

mapping_dict = {
    "properties": {
        "titulo": {"type": "text"},
        "data": {"type": "date"},
        "corpo": {"type": "text"},
    }
}

news = ElasticsearchClient()
news.create_index("noticia", mapping_dict)
news.add_documents(disinformation_news, "noticias")
