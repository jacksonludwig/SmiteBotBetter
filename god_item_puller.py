from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
import time
import db_connector
import re

GODS_URL = "https://www.smitegame.com/gods/"
ITEMS_URL = "https://www.smitefire.com/smite/items"
BASE_BUILD_URL = "https://smite.gg/stats/703/conquest/all/"


def fake_browser(URL):
    page = urllib.request.Request(
        ITEMS_URL, headers={'User-agent': 'Mozilla/5.0'})
    infile = urllib.request.urlopen(page).read()
    data = infile.decode('ISO-8859-1')
    return data


def get_soup(URL):
    source = fake_browser(URL)
    return BeautifulSoup(source, "html.parser")


def fake_browser_selenium(URL):
    adblock_file = "C:\\Users\\Jackson\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\0uicy69o.selenium_prof\\extensions\\uBlock0@raymondhill.net.xpi"
    profile = webdriver.FirefoxProfile(
        "C:\\Users\\Jackson\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\0uicy69o.selenium_prof")
    driver = webdriver.Firefox(
        executable_path=r"geckodriver.exe", firefox_profile=profile)
    driver.install_addon(adblock_file, temporary=True)
    driver.get(URL)
    time.sleep(10)
    return driver.page_source.encode("utf-8").strip()


def get_soup_selenium(URL):
    source = fake_browser_selenium(URL)
    return BeautifulSoup(source, "html.parser")


def write_names_to_text(file_name, names):
    with open(file_name, 'w', encoding='utf-8') as file:
        for name in names:
            file.write(name)
            file.write("\n")


def find_god_names(soup):
    names = []
    for div in soup.find_all('div', class_="details__name"):
        names.append(div.text)
    return names


def find_item_names(soup):
    names = []
    for div in soup.find_all('div', class_="god-name"):
        names.append(div.text)
    return names


def get_god_info():
    gods_soup = get_soup_selenium(GODS_URL)
    god_names = find_god_names(gods_soup)
    write_names_to_text("names.txt", god_names)


def get_item_info():
    item_soup = get_soup(ITEMS_URL)
    item_names = find_item_names(item_soup)
    write_names_to_text("items.txt", item_names)


# This will have to go through siblings of the correct flex class
# Needs finishing
def get_core_build(names):
    for name in names:
        search_name = name.lower()
        soup = get_soup_selenium(BASE_BUILD_URL + search_name)
        print(BASE_BUILD_URL + search_name)
        break


def main():
   # get_item_info()
   # get_god_info()
    list_of_names_from_db = db_connector.query_with_fetchall("god")
    get_core_build(list_of_names_from_db)


main()
