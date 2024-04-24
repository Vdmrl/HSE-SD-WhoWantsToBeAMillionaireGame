from sqlalchemy.orm import mapped_column, Mapped

from db.engine import Base


class Record(Base):
    __tablename__ = "record"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    record: Mapped[int]


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    answer1: Mapped[str]
    answer2: Mapped[str]
    answer3: Mapped[str]
    answer4: Mapped[str]
    right_answer: Mapped[int]
    level: Mapped[int]


