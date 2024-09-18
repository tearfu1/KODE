import asyncio

import aiohttp
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.notes.models import Note


class NoteDAO(BaseDAO):
    model = Note

    async def add(self, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = self.model(**values)
                await self.check_data()
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    async def check_data(self):
        url = "https://speller.yandex.net/services/spellservice.json/checkText"

        async def check_text(text):
            print(text)
            params = {
                'text': text
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    r = await response.json()
                    for mistake in r:
                        correct = mistake['s'][0]
                        bad = mistake['word']
                        print('aa', correct, bad)
                        text = text.replace(bad, correct)
                    return text

        self.title = await check_text(self.title)
        self.content = await check_text(self.content)
