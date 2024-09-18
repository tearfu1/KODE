import aiohttp
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.notes.models import Note


class NoteDAO(BaseDAO):
    model = Note

    @classmethod
    async def add(cls, user, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_values = await cls.check_data(values)
                new_instance = cls.model(author=user, **new_values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def update(cls, user, filter_by, **values):
        async with async_session_maker() as session:
            async with session.begin():
                filter_by['author'] = user
                new_values = await cls.check_data(values)
                query = (
                    sqlalchemy_update(cls.model)
                    .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
                    .values(**new_values)
                    .execution_options(synchronize_session="fetch")
                )
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount

    @staticmethod
    async def check_text(prev_text):
        url = "https://speller.yandex.net/services/spellservice.json/checkText"

        params = {
            'text': prev_text
        }
        text = prev_text
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                r = await response.json()
                for mistake in r:
                    correct = mistake['s'][0]
                    bad = mistake['word']
                    text = text.replace(bad, correct)
        return text

    @classmethod
    async def check_data(cls, values):
        new_values = {
            'title': values['title'],
            'content': values['content'],
        }
        title = await cls.check_text(values['title'])
        content = await cls.check_text(values['content'])
        new_values.update(title=title, content=content)
        return new_values
