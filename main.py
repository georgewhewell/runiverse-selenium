
import threading
import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from session import Session
from sight import image_contains_template

USERNAME = os.environ["RUNIVERSE_USERNAME"]
PASSWORD = os.environ["RUNIVERSE_PASSWORD"]

SCREENSHOT_DIR = "screenshots"

def try_login(driver):
    try:
        elem = driver.find_element(By.ID, "email")
        elem.clear()
        elem.send_keys(USERNAME)
        elem = driver.find_element(By.ID, "password")
        elem.clear()
        elem.send_keys(PASSWORD)
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
    except:
        pass

def try_select_character(driver):
    try:
        elem = driver.find_element(By.XPATH, "//div[normalize-space(text())='select character']")
        elem.click()
        time.sleep(2)
    except:
        pass

def battle(driver):
    elem = driver.find_element(By.CSS_SELECTOR, "body")
    elem.send_keys('41')

def farm_wood(driver):
    # just press E every 10 seconds lol
    # print("farming wood")
    elem = driver.find_element(By.CSS_SELECTOR, "body")
    elem.send_keys('eeeeeeeeeeeeee')

def save_screenshot(driver):
    filename = f"{SCREENSHOT_DIR}/screenshot-{int(time.time())}.png"
    driver.save_screenshot(filename)
    return filename
    
def try_press_continue(driver):
    try:
        elem = driver.find_element(By.XPATH, "//div[normalize-space(text())='continue']")
        elem.click()
        return
    except:
        pass
    try:
        elem = driver.find_element(By.XPATH, "//div[normalize-space(text())='Continue']")
        elem.click()
        return
    except:
        pass
    
def try_press_close(driver):
    try:
        elem = driver.find_element(By.CSS_SELECTOR, "div.Content div div#Disconnect.terms-container.col-xxl-4.col-xl-4.col-lg-4.col-md-8.col-sm-8.col-8.offset-xxl-6.offset-xl-6.offset-lg-6.offset-md-2.offset-sm-2.offset-2 div.close-button div img")
        elem.click()
    except:
        pass

def run_loop(driver):
    screenshot = save_screenshot(driver)

    print("checking login")
    try_login(driver)

    print("checking if we need to select character")
    try_select_character(driver)

    print("checking if need to press continue")
    try_press_continue(driver)

    print("checking if need to press close")
    try_press_close(driver)

    print("checking images")
    contains = image_contains_template(screenshot, "battlebar.png")
    if contains.any():
        print(f"{screenshot} contains battlebar.png")
        battle(driver)
        return
    
    contains = image_contains_template(screenshot, "cut_tree.png")
    if contains.any():
        print(f"{screenshot} contains cut_tree.png")
        print("farming wood")
        farm_wood(driver)
        return
    
    contains = image_contains_template(screenshot, "scissors.png")
    if contains.any():
        print(f"{screenshot} contains scissors.png")
        print("farming hemp")
        farm_wood(driver)
        return
        
    contains = image_contains_template(screenshot, "mine.png")
    if contains.any():
        print(f"{screenshot} contains mine.png")
        print("mining")
        farm_wood(driver)
        return
    
    contains = image_contains_template(screenshot, "gas.png")
    if contains.any():
        print(f"{screenshot} contains gas.png")
        print("huffing")
        farm_wood(driver)
        return
        
    contains = image_contains_template(screenshot, "hammer.png")
    if contains.any():
        print(f"{screenshot} contains hammer.png")
        print("hammering")
        farm_wood(driver)
        return
    
    contains = image_contains_template(screenshot, "mob-alert-light.png")
    if contains.any():
        print(f"mob alert at {contains}")
        [x,y] = contains[0]
        print(f"moving to {x},{y}")
        el=driver.find_element(By.CSS_SELECTOR, "body")

        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(el, x, y)
        action.click()
        action.perform()
                

if __name__ == "__main__":
    try:
        session = Session.load()
    except:
        session = Session.new_firefox()
        session.save()

    # check if we need to login
    print("loading driver")
    driver = session.driver()
    # spawn_screenshot_timer_thread(driver, 1)
    # breakpoint()
    while True:
        print("starting loop")
        try:
            run_loop(driver)
        except Exception as e:
            print("exception in loop: ", e)
            # driver.
            # farm_wood(driver)
        
        time.sleep(1)
    # start screenshot thread
