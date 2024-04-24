from typing import Tuple

from sqlalchemy import select

from db.engine import async_session_factory
from db.models.game import Record, Question

from random import choice

win_amounts = [500, 1000, 2000, 3000, 5000, 10000, 15000, 25000, 50000, 100000, 200000, 400000, 800000, 1500000, 3000000]

class Game:
    def __init__(self):
        self._round = 0
        self._right_answer = None

    @property
    def round(self):
        return self._round

    async def get_question(self) -> Tuple[str]:
        """
        choose current question
        :return: (question, ans1, ans2, ans3, ans4))
        """
        async with async_session_factory() as session:
            query = (select(Question).where(Question.level == self._round + 1))
            result = await session.execute(query)
            questions = result.scalars().all()
            if questions:
                question = choice(questions)
                self._right_answer = question.right_answer
                return tuple([question.text, question.answer1, question.answer2, question.answer3, question.answer4])
            else:
                return None



    def give_answer(self, ans: int) -> None:
        if ans == self._right_answer:
            self._round += 1
        else:
            self._round = 0
        print(f"{self._round}")


