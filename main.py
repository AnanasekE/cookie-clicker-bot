import time

from selenium import webdriver
from selenium.common import InvalidArgumentException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def setup():
    web_driver = webdriver.Chrome()

    web_driver.get("https://orteil.dashnet.org/cookieclicker/")
    time.sleep(1)

    button = web_driver.find_element(By.CLASS_NAME, "fc-button-label")
    button.click()

    button = web_driver.find_element(By.ID, "langSelect-EN")
    button.click()

    time.sleep(5)
    button = web_driver.find_element(By.ID, "bigCookie")
    for _ in range(100):
        button.click()

    button = web_driver.find_element(By.ID, "product0")
    button.click()

    return web_driver


def get_money_per_second_to_cost_ratio(element: WebElement) -> float:
    product_id = element.id[-1]
    price = element.find_element(By.ID, "productPrice" + product_id)
    print(price)
    return 0.0


def get_current_money():
    driver.find_element(By.ID, "cookies")
    return int(driver.execute_script("return Game.cookies"))


def buy_building(building_number: int):
    building_button: WebElement = driver.find_element(By.ID, f"product{building_number}")
    building_button.click()


class Building:
    def __init__(self, element: WebElement):
        self.element: WebElement = element


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


def get_available_upgrades():
    return driver.find_element(By.ID, "upgrades").find_elements(By.CLASS_NAME, "enabled")


def run_game_loop(big_cookie_button: WebElement):
    money = get_current_money()

    best_building = get_best_building()
    if best_building and money >= best_building['price']:
        buy_building(best_building['id'])

    try:
        get_available_upgrades()[0].click()
    except InvalidArgumentException:
        pass
    except IndexError:
        pass

    big_cookie_button.click()


driver = setup()
while True:
    run_game_loop(driver.find_element(By.ID, "bigCookie"))
