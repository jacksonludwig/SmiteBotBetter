from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
import time
import db_connector
import re
import utils

GODS_URL = "https://www.smitegame.com/gods/"
ITEMS_URL = "https://www.smitefire.com/smite/items"
BASE_BUILD_URL = "https://smite.gg/stats/703/conquest/all/"

CATEGORIES = ["Core", "Offensive", "Defensive"]


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
    profile.set_preference("browser.privatebrowsing.autostart", True)
    driver = webdriver.Firefox(
        executable_path=r"geckodriver.exe", firefox_profile=profile)
    driver.install_addon(adblock_file, temporary=True)
    driver.get(URL)
    time.sleep(5)
    data = driver.page_source.encode("utf-8").strip()
    driver.quit()
    return data


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


def get_core(soup):
    build = []
    core_div = soup.find("div", string=CATEGORIES[0])
    for sibling in core_div.next_siblings:
        data = sibling.find("div", title=True)
        build.append(data.text)
    return build


def get_offensive(soup):
    build = []
    core_div = soup.find("div", string=CATEGORIES[1])
    for sibling in core_div.next_siblings:
        data = sibling.find("div", title=True)
        build.append(data.text)
    return build


def get_defensive(soup):
    build = []
    core_div = soup.find("div", string=CATEGORIES[2])
    for sibling in core_div.next_siblings:
        data = sibling.find("div", title=True)
        build.append(data.text)
    return build


def get_build(name):
    search_name = name.lower()
    search_name = utils.remove_non_letters(search_name)
    print(f"God name: {name}")
    print(f"Fetching from: {BASE_BUILD_URL}{search_name}")
    soup = get_soup_selenium(BASE_BUILD_URL + search_name)
    core_build = get_core(soup)
    offensive_build = get_offensive(soup)
    defensive_build = get_defensive(soup)
    print(
        f"Build received: {len(core_build) + len(offensive_build) + len(defensive_build)} items")
    return [core_build, offensive_build, defensive_build]


def insert_to_db(list_of_builds, item_dict, name_dict, name, category):
    for item in list_of_builds[category]:
        i = item_dict.get(item)
        if i is not None:
            n = name_dict.get(utils.replace_dashes_with_spaces(name))
            db_connector.insert_into_build(n, category, i)
            print(i)


def insert_all_to_db_in_range(list_of_names_from_db, item_dict, name_dict, start, end):
    for i in range(start, end):
        if list_of_names_from_db[i] == "Baba-Yaga":
            continue
        list_of_builds = get_build(list_of_names_from_db[i])
        for j in range(3):
            insert_to_db(list_of_builds, item_dict, name_dict,
                         list_of_names_from_db[i], j)


def insert_all_to_db(list_of_names_from_db, item_dict, name_dict):
    for name in list_of_names_from_db:
        if name == "Baba-Yaga":
            continue
        list_of_builds = get_build(name)
        for i in range(3):
            insert_to_db(list_of_builds, item_dict, name_dict, name, i)


def main():
    list_of_names_from_db = db_connector.query_with_fetchall("god")
    list_of_items_from_db = db_connector.query_with_fetchall("item")
    name_dict = utils.create_dictionary_from_list(list_of_names_from_db)
    item_dict = utils.create_dictionary_from_list(list_of_items_from_db)
    utils.replace_spaces_with_dashes(list_of_names_from_db)

    insert_all_to_db(list_of_names_from_db, item_dict, name_dict)


main()
