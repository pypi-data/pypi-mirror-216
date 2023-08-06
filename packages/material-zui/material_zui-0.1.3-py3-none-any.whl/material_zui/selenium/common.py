from typing import Any
from selenium.webdriver.common.by import By


def safe_find_element(parent: Any, by: str = By.ID,
                      value: str | None = None):
    try:
        return parent.find_element(by, value)
    except:
        return None
