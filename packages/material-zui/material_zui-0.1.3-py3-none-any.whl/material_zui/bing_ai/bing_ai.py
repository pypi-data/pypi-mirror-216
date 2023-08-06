from pathlib import Path
from time import sleep
from typing import Any
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
from EdgeGPT.EdgeUtils import Query, ImageQuery, Cookie

from material_zui.file import write_excel, ZuiExcelColumns
from .result import ZuiBingAiResult
from .type import ZuiArticle


class ZuiBingAi:
    creative = ConversationStyle.creative
    balanced = ConversationStyle.balanced
    precise = ConversationStyle.precise

    def __init__(self, directory_cookie_path: str = '') -> None:
        '''
        - Base on https://pypi.org/project/EdgeGPT
        @directory_cookie_path: `directory path` of cookie file (file cookie must have pattern `bing_cookies_*.json`)
        - In case only ask, DO NOT NEED to login for regions allow using free Bing chat AI (support `Vietnam`), but sometimes reseponse required login
        - If meet error `EdgeGPT.exceptions.NotAllowedToAccess: Sorry, you need to login first to access this service.`, just try again
        '''
        self.response: dict[Any, Any] = {}
        if directory_cookie_path:
            self.set_cookie(directory_cookie_path)

    def set_cookie(self, directory_cookie_path: str) -> None:
        self.directory_cookie_path = Path(directory_cookie_path).resolve()
        Cookie.dirpath = self.directory_cookie_path

    async def create(self):
        self.bot = await Chatbot.create()

    async def ask(self, prompt: str, conversation_style: ConversationStyle = ConversationStyle.creative) -> ZuiBingAiResult:
        '''
        In case only ask, DO NOT NEED to login for regions allow using free Bing chat AI (support `Vietnam`)
        '''
        if not hasattr(self, 'bot'):
            await self.create()
        self.response = await self.bot.ask(prompt=prompt, conversation_style=conversation_style)
        return ZuiBingAiResult(self.response)

    def query(self, prompt: str, style: str = "balanced", directory_cookie_path: str = ''):
        '''
        @style: including `creative`, `balanced`, `precise`
        @directory_cookie_path: directory of cookie file (file cookie must have pattern `bing_cookies_*.json`)
        '''
        if directory_cookie_path:
            self.set_cookie(directory_cookie_path)
        self.responseQuery = Query(prompt, style=style)
        self.response = self.responseQuery.response  # type: ignore
        return ZuiBingAiResult(self.response)  # type: ignore

    def gen_image(self, prompt: str):
        '''
        Must input cookie to use this feature
        '''
        # Cookie.image_dirpath
        return ImageQuery(prompt)

    def gen_article(self, topics: list[str]) -> list[ZuiArticle]:
        data = []
        for index, topic in enumerate(topics):
            find_keywords = f'Identify 10 SEO keywords related to {topic}'
            keywords = self.query(find_keywords)
            data.append({
                'title': index,
                'description': 'description',
                'content': 'content',
                'keywords': keywords.last_text,
            })
            sleep(200)
        return data

    def article_to_excel(self, file_path: str, topics: list[str]) -> None:
        columns: ZuiExcelColumns = [
            {'field': 'title', 'name': 'title'},
            {'field': 'description', 'name': 'Description'},
            {'field': 'content', 'name': 'Content'},
            {'field': 'keywords', 'name': 'Keywords'},
        ]
        data: list[Any] = self.gen_article(topics)
        write_excel(file_path, columns, data)
