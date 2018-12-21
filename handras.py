from bs4 import BeautifulSoup
import requests
import time


def main():
    for page in range(0, 365):
        parse_listing_page(get_url(page))


def get_url(page):
    return "http://handras.hu/page/" + str(page) 


def get_page(url):
    return BeautifulSoup(requests.get(url).text, "lxml")


def parse_article_page(link):
    if link is not None:
        article = BeautifulSoup(link)
        print(article.find("h2").text)
        print(article.find("time", datetime=True)["datetime"])
        print(remove_elements(article.find("div", class_="entry__body")))


def remove_elements(content):
    for element in ["essb_links"]:
        element_in_soup = content.find("div", class_=element)
        if element_in_soup is not None:
            element_in_soup.decompose()
    
    return content


def parse_listing_page(url):
    for link in get_page(url).select("h2.entry__title a"):
        parse_article_page(requests.get(link.get("href")).text)
        time.sleep(1)


if __name__ == "__main__":
    main()
