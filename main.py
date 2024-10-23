import json
import time
from json.encoder import INFINITY

from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from setuptools.command.build import build


class State:
    CLICKING = 0
    OTHER = 1


def get_money_per_second_to_cost_ratio(element: WebElement) -> float:
    product_id = element.id[-1]
    price = element.find_element(By.ID, "productPrice" + product_id)
    print(price)
    return 0.0


driver = webdriver.Chrome()

driver.get("https://orteil.dashnet.org/cookieclicker/")
time.sleep(1)

button = driver.find_element(By.CLASS_NAME, "fc-button-label")
button.click()

button = driver.find_element(By.ID, "langSelect-EN")
button.click()

time.sleep(5)
button = driver.find_element(By.ID, "bigCookie")
for _ in range(100):
    button.click()

button = driver.find_element(By.ID, "product0")
button.click()


def get_current_money():
    driver.find_element(By.ID, "cookies")
    return int(driver.execute_script("return Game.cookies"))


def buy_building(building_number: int):
    building_button: WebElement = driver.find_element(By.ID, f"product{building_number}")
    building_button.click()


class Building:
    def __init__(self, element: WebElement):
        self.element: WebElement = element

    def price(self):
        elem = self.element.find_element(By.CLASS_NAME, "price")
        return int(elem.text)


def get_buildings():
    buildings = driver.execute_script("""
        return Object.values(Game.ObjectsById).map(function(building) {
            return {
                id: building.id,
                price: building.price,
                cps: building.cps(this) || building.storedCps,
                amount: building.amount,
                locked: building.locked
            };
        });
    """)
    return buildings


def get_best_building():
    buildings = get_buildings()
    filter(lambda x: x['locked'] == 0, buildings)
    buildings.sort(key=lambda x: x['cps'] / x['price'], reverse=True)
    return buildings[0]


def get_upgrades():
    return driver.execute_script('''
    return Object.values(Game.UpgradesById).map(function(upgrade) {
            return {
                price: upgrade.basePrice
            };
        });
    ''')


def get_price_for_upgrade(upgrade_id: int) -> int:
    return get_upgrades()[upgrade_id]


def get_best_upgrade_price():
    store: WebElement = driver.find_element(By.ID, "upgrades")
    elements = store.find_elements(By.CLASS_NAME, "enabled")
    if len(elements) > 0:
        upgrade_id = elements[0].get_property("data-id")
        price = get_price_for_upgrade(upgrade_id)
        return price
    return INFINITY


def buy_best_upgrade():
    store: WebElement = driver.find_element(By.ID, "upgrades")
    elements = store.find_elements(By.CLASS_NAME, "enabled")

    try:
        elements[0].click()
    except StaleElementReferenceException:
        return
    except IndexError:
        return


def run_game_loop(big_cookie_button: WebElement):
    money = get_current_money()
    best_building = get_best_building()

    if best_building:
        if money >= best_building['price']:
            buy_best_upgrade()
            buy_building(best_building['id'])

    if money >= get_best_upgrade_price():
        buy_best_upgrade()

    big_cookie_button.click()


while True:
    run_game_loop(driver.find_element(By.ID, "bigCookie"))
