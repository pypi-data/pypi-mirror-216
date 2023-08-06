from typing import Any

from material_zui.list import map_to, filter_to
from material_zui.string import not_empty


class ZuiBingAiResult():
    def __init__(self, response: dict[Any, Any]) -> None:
        self.response = response

    def get_valid_message(self, messages: list[str]) -> list[str]:
        return filter_to(messages, lambda text, _: not_empty(text))

    @property
    def full_texts(self) -> list[str]:
        texts: list[str] = map_to(self.response["item"]["messages"],
                                  lambda message, _: message.get('text') or message.get('hiddenText'))
        return self.get_valid_message(texts)

    @property
    def texts(self) -> list[str]:
        texts: list[str] = map_to(self.response["item"]["messages"],
                                  lambda message, _: message.get('text'))
        return self.get_valid_message(texts)

    @property
    def last_text(self) -> str:
        return self.texts.pop()
