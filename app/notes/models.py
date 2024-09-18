from sqlalchemy.orm import Mapped

from app.database import Base, int_pk


class Note(Base):
    id: Mapped[int_pk]
    title: Mapped[str]
    content: Mapped[str]

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.title!r}")

    def __repr__(self):
        return str(self)


