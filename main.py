import json
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


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
time.sleep(0.5)

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
    json_string = driver.execute_script("return Game.ObjectsById")
    return json.load(json_string)


def get_best_building():
    buildings = get_buildings()
    buildings_cps = json.load(driver.execute_script('Game.ObjectsById.map(obj => obj.cps())'))


def run_game_loop(state: int, big_cookie_button: WebElement):
    # Check if player has enough money to buy the next upgrade
    # if yes buy it and start clicking again
    # if not run gameloop to buy
    money = get_current_money()
    get_best_building()
    buy_building(0)
    # bestElement: Building
    # while money < bestElement.price()
    #     big_cookie_button.click()
    pass


run_game_loop(State.CLICKING, driver.find_element(By.ID, "bigCookie"))

time.sleep(100)
