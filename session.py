import json
from pydantic import BaseModel
from selenium import webdriver

SELENIUM_URL = "http://localhost:4444/wd/hub"

class Session(BaseModel):
    selenium_url: str
    selenium_token: str

    @classmethod
    def new_firefox(cls):
        driver = webdriver.Remote(
            command_executor=SELENIUM_URL,
            options=webdriver.FirefoxOptions()
        )
        driver.get("https://game.runiverse.world/")
        return cls(
            selenium_url=driver.command_executor._url,
            selenium_token=driver.session_id,
        )
    
    @classmethod
    def load(cls):
        return cls(**json.load(open("session.json")))

    def save(self) -> None:
        json.dump(self.dict(), open("session.json", "w"))

    def driver(self):
        driver = webdriver.Remote(
            command_executor=SELENIUM_URL,
            options=webdriver.FirefoxOptions()
        )
        driver.close()
        driver.session_id = self.selenium_token
        return driver

