from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import os


def get_db_name():
    return "handras.db"


def delete_db_file():
    if os.path.isfile(get_db_name()):
        os.remove(get_db_name())


def get_sqlite_connection():
    return sqlite3.connect("handras.db")


def create_db_schema():
    delete_db_file()
    get_sqlite_connection().executescript(
        """
        CREATE TABLE IF NOT EXISTS articles (Title Varchar, Date Varchar, Body Varchar);
        CREATE TABLE IF NOT EXISTS error_log (Message Varchar);
        """
    )


def execute_sql(sql):
    connection = get_sqlite_connection()
    connection.cursor().execute(sql)
    connection.commit()


def main():
    create_db_schema()
    for page in range(0, 365):
        parse_listing_page(get_url(page))


def get_request(url):
    try:
        return requests.get(url)
    except requests.exceptions.RequestException as e:
        execute_sql("INSERT INTO error_log VALUES ('Request error: {}');".format(e))


def get_url(page):
    return "http://handras.hu/page/" + str(page) 


def get_page(url):
    return BeautifulSoup(get_request(url).text, "lxml")


def parse_article_page(link):
    article = BeautifulSoup(link, "lxml")
    title = article.find("h2").text
    date = article.find("time", datetime=True)["datetime"]
    body = remove_elements(article.find("div", class_="entry__body"))
    body = str(body).replace("'", "")

    execute_sql("INSERT INTO articles VALUES ('{0}', '{1}', '{2}');".format(title, date, body))


def remove_elements(content):
    for element in ["essb_links"]:
        element_in_soup = content.find("div", class_=element)
        if element_in_soup is not None:
            element_in_soup.decompose()
    
    return content


def parse_listing_page(url):
    for link in get_page(url).select("h2.entry__title a"):
        parse_article_page(get_request(link.get("href")).text)
        time.sleep(1)


if __name__ == "__main__":
    main()
