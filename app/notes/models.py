from sqlalchemy.orm import Mapped

from app.database import Base, int_pk


class Note(Base):
    id: Mapped[int_pk]
    title: Mapped[str]
    content: Mapped[str]
    author: Mapped[str]

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"title={self.title!r},"
                f"content={self.content!r},"
                f"author={self.author!r})")

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
